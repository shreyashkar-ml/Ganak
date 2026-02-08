
from backends.backend_interface import RunnerBackend, RunnerJob


class DockerBackend(RunnerBackend):
    """Docker backend placeholder for Option C."""

    def submit_job(self, job: RunnerJob) -> None:
        if not isinstance(job, RunnerJob):
            raise TypeError("job must be RunnerJob")
        raise NotImplementedError("Docker backend not implemented")

    def cancel_job(self, job_id: str) -> None:
        if not isinstance(job_id, str):
            raise TypeError("job_id must be str")
        raise NotImplementedError("Docker backend not implemented")

