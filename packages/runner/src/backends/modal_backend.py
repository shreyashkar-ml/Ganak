from __future__ import annotations

from backends.backend_interface import RunnerBackend, RunnerJob


class ModalBackend(RunnerBackend):
    """Modal backend placeholder for Phase 0."""

    def submit_job(self, job: RunnerJob) -> None:
        if not isinstance(job, RunnerJob):
            raise TypeError("job must be RunnerJob")
        raise NotImplementedError("Modal backend submission not wired")

    def cancel_job(self, job_id: str) -> None:
        if not isinstance(job_id, str):
            raise TypeError("job_id must be str")
        raise NotImplementedError("Modal backend cancellation not wired")

