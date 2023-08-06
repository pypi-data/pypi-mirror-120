"""Library to initiate backend RIME service requests."""

import time
from datetime import datetime
from typing import Any, Dict, List, NamedTuple, Optional

import grpc
import simplejson
from google.protobuf.json_format import MessageToDict

from rime_sdk.internal.throttle_queue import ThrottleQueue
from rime_sdk.protos.model_testing_pb2 import (
    CustomImage,
    GetLatestLogsRequest,
    GetTestJobRequest,
    JobMetadata,
    JobStatus,
    ListTestJobsRequest,
    StartStressTestRequest,
)
from rime_sdk.protos.model_testing_pb2_grpc import ModelTestingStub
from rime_sdk.protos.results_upload_pb2 import (
    CreateProjectRequest,
    VerifyProjectIDRequest,
)
from rime_sdk.protos.results_upload_pb2_grpc import ResultsStoreStub


class RIMEStressTestJob:
    """An interface to a RIME stress testing job."""

    def __init__(self, model_testing_addr: str, job_name: str) -> None:
        """Create a new RIME Job.

        Args:
            model_testing_addr: str
                Address of a RIME ModelTesting gRPC service.
            job_name: str
                The name of the RIME job that this object monitors.
        """
        self._job_name = job_name
        self._model_testing_channel = grpc.insecure_channel(model_testing_addr)
        self._model_testing_client = ModelTestingStub(self._model_testing_channel)

    def __del__(self) -> None:
        """Destroy the client's connection to the RIME backend."""
        self._model_testing_channel.close()

    def __eq__(self, obj: Any) -> bool:
        """Check if this job is equivalent to 'obj'."""
        # Always compare start times in UTC timezone for consistency in tests.
        return isinstance(obj, RIMEStressTestJob) and self._job_name == obj._job_name

    def get_status(
        self,
        verbose: bool = False,
        wait_until_finish: bool = False,
        poll_rate_sec: float = 5.0,
    ) -> Dict:
        """Query the ModelTest service for the job's status.

        This query includes an option to wait until the job is finished.
        It will either have succeeded or failed.

        Arguments:
            verbose: bool
                whether or not to print diagnostic information such as logs.
            wait_until_finish: bool
                whether or not to block until the job is SUCCEEDED or FAILED.
            poll_rate_sec: float
                the frequency with which to poll the job's status.

        Returns:
            A dictionary representing the job's state.
        """
        jobReq = GetTestJobRequest(job_name=self._job_name)
        try:
            job: JobMetadata = self._model_testing_client.GetTestJob(jobReq).job
        except grpc.RpcError as e:
            # TODO(QuantumWombat): distinguish errors
            raise ValueError(e)
        if verbose:
            print(
                "Job '{}' started at {}".format(
                    job.name, datetime.fromtimestamp(job.start_time_secs)
                )
            )

        # Do not repeat if the job is finished or blocking is disabled.
        while wait_until_finish and not job.status in (
            JobStatus.SUCCEEDED,
            JobStatus.FAILING,
        ):
            try:
                job = self._model_testing_client.GetTestJob(jobReq).job
            except grpc.RpcError as e:
                # TODO(QuantumWombat): distinguish errors
                raise ValueError(e)
            if verbose:
                minute, second = divmod(job.running_time_secs, 60)
                hour, minute = divmod(minute, 60)
                print(
                    "Status: {}, Running Time: {:02}:{:02}:{:05.2f}".format(
                        JobStatus.Name(job.status), int(hour), int(minute), second
                    )
                )
            time.sleep(poll_rate_sec)

        # Only get the logs if verbose is enabled and the job is finished.
        if verbose and job.status in (JobStatus.SUCCEEDED, JobStatus.FAILING):
            logReq = GetLatestLogsRequest(job_name=self._job_name)
            try:
                for logRes in self._model_testing_client.GetLatestLogs(request=logReq):
                    print(logRes.chunk, end="")
            except grpc.RpcError as e:
                # TODO(QuantumWombat): distinguish errors
                raise ValueError(e)

        return MessageToDict(job)


class RIMEProject(NamedTuple):
    """Information about a RIME project."""

    project_id: str
    name: str
    description: str


class RIMEClient:
    """RIMEClient provides an interface to RIME backend services."""

    # A throttler that limits the number of model tests to roughly 20 every 5 minutes.
    # This is a static variable for RIMEClient.
    _throttler = ThrottleQueue(desired_events_per_epoch=20, epoch_duration_sec=300)

    def __init__(self, domain: str, channel_timeout: float = 5.0) -> None:
        """Create a new RIMEClient connected to the services available at `domain`.

        Args:
            domain: str
                The base domain/address of the RIME service.+
            channel_timeout: float
                The amount of time to wait for channels to become ready
                when opening connections to gRPC servers.

        Raises:
            ValueError
                If a connection cannot be made to a backend service within `timeout`.
        """
        self._model_testing_addr = self._get_model_testing_addr(domain)
        upload_addr = self._get_upload_addr(domain)
        self._model_testing_channel = self._build_and_validate_channel(
            self._model_testing_addr, channel_timeout
        )
        self._model_testing_client = ModelTestingStub(self._model_testing_channel)
        self._upload_channel = self._build_and_validate_channel(
            upload_addr, channel_timeout
        )
        self._upload_client = ResultsStoreStub(self._upload_channel)

    def _get_model_testing_addr(self, domain: str) -> str:
        """Construct an address to the model-testing service from `domain`.

        Args:
            domain: str
                The base domain/address of the RIME service.
        """
        return f"modeltesting.{domain}:80"

    def _get_upload_addr(self, domain: str) -> str:
        """Construct an address to the upload service from `domain`.

        Args:
            domain: str
                The base domain/address of the RIME service.
        """
        return f"results-store.{domain}:80"

    def _build_and_validate_channel(self, addr: str, timeout: float) -> grpc.Channel:
        """Build and validate an insecure gRPC channel at `addr`.

        Args:
            addr: str
                The address of the RIME gRPC service.
            timeout: float
                The amount of time to wait for the channel to become ready.

        Raises:
            ValueError
                If a connection cannot be made to a backend service within `timeout`.
        """
        try:
            channel = grpc.insecure_channel(addr)
            grpc.channel_ready_future(channel).result(timeout=timeout)
            return channel
        except grpc.FutureTimeoutError:
            raise ValueError(f"Could not connect to server at address `{addr}`")

    def __del__(self) -> None:
        """Destroy the client's connection to the RIME backend."""
        self._model_testing_channel.close()
        self._upload_channel.close()

    # TODO(QuantumWombat): do this check server-side
    def _project_exists(self, project_id: str) -> bool:
        """Check if `project_id` exists.

        Args:
            project_id: the id of the project to be checked.

        Returns:
            whether or not project_id is a valid project.

        Raises:
            grpc.RpcError if the server has an error while checking the project.
        """
        verify_req = VerifyProjectIDRequest(project_id=project_id)
        try:
            self._upload_client.VerifyProjectID(verify_req)
            return True
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.NOT_FOUND:
                return False
            raise rpc_error

    def create_project(self, name: str, description: str) -> RIMEProject:
        """Create a new RIME project in RIME's backend.

        Args:
            name: str
                Name of the new project.
            description: str
                Description of the new project.

        Returns:
            A RIMEProject providing information about the new project.

        Raises:
            ValueError
                If the request to the Upload service failed.
        """
        req = CreateProjectRequest(name=name, description=description)
        try:
            resp = self._upload_client.CreateProject(request=req)
            return RIMEProject(
                project_id=resp.id, name=resp.name, description=resp.description
            )
        except grpc.RpcError as e:
            # TODO(blaine): differentiate on different error types.
            raise ValueError(e)

    def start_stress_test(
        self,
        test_run_config: dict,
        project_id: Optional[str] = None,
        custom_image: Optional[CustomImage] = None,
    ) -> RIMEStressTestJob:
        """Start a RIME model stress test on the backend's ModelTesting service.

        Args:
            test_run_config: dict
                Configuration for the test to be run, which specifies paths to
                the model and datasets to used for the test.
            project_id: Optional[str]
                Identifier for the project where the resulting test run will be stored.
                If not specified, the results will be stored in the default project.
            custom_image: Optional[CustomImage]
                Specification of a customized container image to use running the model
                test. The image must have all dependencies required by your model.
                The image must specify a name for the image and optional a pull secret
                (of type CustomImage.PullSecret) with the name of the kubernetes pull
                secret used to access the given image.

        Returns:
            A RIMEStressTestJob providing information about the model stress test job.

        Raises:
            ValueError
                If the request to the ModelTest service failed.

        TODO(blaine): Add config validation service.
        """
        if not isinstance(test_run_config, dict):
            raise ValueError("The configuration must be a dictionary")

        if project_id and not self._project_exists(project_id):
            raise ValueError("Project id {} does not exist".format(project_id))

        req = StartStressTestRequest(
            test_run_config=simplejson.dumps(test_run_config).encode(),
        )
        if project_id:
            req.project_id = project_id
        if custom_image:
            req.testing_image.CopyFrom(custom_image)
        try:
            RIMEClient._throttler.throttle(
                throttling_msg="Your request is throttled to limit # of model tests."
            )
            job: JobMetadata = self._model_testing_client.StartStressTest(
                request=req
            ).job
            return RIMEStressTestJob(self._model_testing_addr, job.name)
        except grpc.RpcError as e:
            # TODO(blaine): differentiate on different error types.
            raise ValueError(e)

    def list_stress_test_jobs(
        self,
        status_filters: Optional[List[str]] = None,
        project_id: Optional[str] = None,
    ) -> List[RIMEStressTestJob]:
        """Query the ModelTest service for a list of jobs.

        Args:
            status_filters: Optional[List[str]]
                Filter for selecting jobs by a union of statuses.
                The following list enumerates all acceptable values.
                ['UNKNOWN_JOB_STATUS', 'PENDING', 'RUNNING', 'FAILING', 'SUCCEEDED']
                If omitted, jobs will not be filtered by status.
            project_id: Optional[str]
                Filter for selecting jobs by project ID.
                If omitted, jobs from all projects will be returned.

        Returns:
            A list of JobMetadata objects serialized to JSON.

        Raises:
            ValueError
                If the provided status_filters array has invalid values.
                If the request to the ModelTest service failed.
        """
        req = ListTestJobsRequest()
        if status_filters:
            # This throws a ValueError if status is not a valid JobStatus enum value.
            # TODO(QuantumWombat): should we catch the error and show something more interpretable?
            # It looks like -> ValueError: Enum JobStatus has no value defined for name 'yeezus'
            req.selected_statuses.extend(
                [JobStatus.Value(status) for status in status_filters]
            )
        if project_id and not self._project_exists(project_id):
            raise ValueError("Project id {} does not exist".format(project_id))
        if project_id:
            req.project_id = project_id
        try:
            res = self._model_testing_client.ListTestJobs(req)
            return [
                RIMEStressTestJob(self._model_testing_addr, job_name=job.name)
                for job in res.jobs
            ]
        except grpc.RpcError as e:
            raise ValueError(e)
