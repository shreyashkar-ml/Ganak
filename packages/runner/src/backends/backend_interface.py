from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class RunnerJob:
    job_id: str
    session_id: str
    run_id: str
    snapshot_id: str


class RunnerBackend(ABC):
    """Backend interface for executing runner jobs."""

    @abstractmethod
    def submit_job(self, job: RunnerJob) -> None:
        raise NotImplementedError

    @abstractmethod
    def cancel_job(self, job_id: str) -> None:
        raise NotImplementedError