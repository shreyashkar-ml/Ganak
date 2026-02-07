from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class RunnerJob:
    job_id: str
    session_id: str
    run_id: str
    snapshot_id: str


class RunnerBackend(Protocol):
    """Backend interface for executing runner jobs."""

    def submit_job(self, job: RunnerJob) -> None:
        ...

    def cancel_job(self, job_id: str) -> None:
        ...

