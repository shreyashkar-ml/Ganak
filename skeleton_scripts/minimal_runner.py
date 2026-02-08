"""Minimal runner skeleton."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from minimal_agent_core import (
    AgentInput,
    EventLog,
    RunPolicy,
    ScopePolicy,
    StopController,
    ToolRegistry,
    run_agent_loop,
)


@dataclass(frozen=True)
class SnapshotRequest:
    """Snapshot request."""

    repo_id: str
    commit: str


@dataclass(frozen=True)
class SnapshotResult:
    """Snapshot result."""

    snapshot_id: str


def build_snapshot(request: SnapshotRequest) -> SnapshotResult:
    """Build deterministic snapshot ID."""
    if not isinstance(request, SnapshotRequest):
        raise TypeError("request must be SnapshotRequest")
    return SnapshotResult(snapshot_id=f"{request.repo_id}-{request.commit}")


@dataclass(frozen=True)
class RunnerJob:
    """Runner job contract."""

    job_id: str
    session_id: str
    run_id: str
    snapshot_id: str


class RunnerBackend(ABC):
    """Mandatory runner backend interface."""

    @abstractmethod
    def submit_job(self, job: RunnerJob) -> None:
        """Submit one runner job."""
        raise NotImplementedError

    @abstractmethod
    def cancel_job(self, job_id: str) -> None:
        """Cancel one runner job."""
        raise NotImplementedError


class RunnerStateInterface(ABC):
    """State operations required by runner backend."""

    @abstractmethod
    def get_run(self, run_id: str) -> Any:
        """Return run object by ID."""
        raise NotImplementedError

    @abstractmethod
    def update_run_status(self, run_id: str, status: str) -> None:
        """Update run status."""
        raise NotImplementedError

    @abstractmethod
    def mark_run_complete(self) -> None:
        """Update dispatch bookkeeping when run completes."""
        raise NotImplementedError

    @abstractmethod
    def append_event(self, event_type: str, session_id: str, run_id: str, payload: dict[str, Any]) -> None:
        """Append one event to state log."""
        raise NotImplementedError

    @abstractmethod
    def get_event_log(self) -> EventLog:
        """Return event log used by the agent loop."""
        raise NotImplementedError


@dataclass
class LocalRunnerBackend(RunnerBackend):
    """In-process runner backend."""

    state: RunnerStateInterface
    tool_registry: ToolRegistry
    scope_policy: ScopePolicy
    submitted_jobs: dict[str, RunnerJob] = None
    active_jobs: set[str] = None
    completed_jobs: set[str] = None
    cancel_requests: set[str] = None

    def __post_init__(self) -> None:
        """Initialize local runtime bookkeeping."""
        self.submitted_jobs = {}
        self.active_jobs = set()
        self.completed_jobs = set()
        self.cancel_requests = set()

    def submit_job(self, job: RunnerJob) -> None:
        """Execute one run immediately."""
        if not isinstance(job, RunnerJob):
            raise TypeError("job must be RunnerJob")
        self.submitted_jobs[job.job_id] = job
        self.active_jobs.add(job.job_id)
        run = self.state.get_run(job.run_id)
        if job.job_id in self.cancel_requests:
            self.state.update_run_status(job.run_id, "canceled")
            self.state.append_event("run_canceled", run.session_id, run.id, {"job_id": job.job_id, "reason": "pre_start"})
            self._finish_job(job.job_id)
            return
        agent_input = AgentInput(session_id=job.session_id, run_id=job.run_id, prompt=run.prompt)
        result = run_agent_loop(
            agent_input=agent_input,
            tool_registry=self.tool_registry,
            scope_policy=self.scope_policy,
            event_log=self.state.get_event_log(),
            policy=RunPolicy(max_steps=6),
            stop_controller=StopController(),
        )
        self.state.update_run_status(job.run_id, "finished" if not result.stopped else "stopped")
        self._finish_job(job.job_id)

    def cancel_job(self, job_id: str) -> None:
        """Cancel a submitted runner job.

        This minimal backend is synchronous, so most cancels will either:
        - mark pre-start cancellation (if request is registered before submit), or
        - be ignored if the job already completed.
        """
        if not isinstance(job_id, str):
            raise TypeError("job_id must be str")
        if job_id in self.completed_jobs:
            return None
        self.cancel_requests.add(job_id)
        job = self.submitted_jobs.get(job_id)
        if job is None:
            return None
        run = self.state.get_run(job.run_id)
        if run.status in {"finished", "stopped", "failed", "canceled"}:
            self._finish_job(job_id)
            return None
        self.state.update_run_status(job.run_id, "canceled")
        self.state.append_event("run_canceled", run.session_id, run.id, {"job_id": job_id, "reason": "requested"})
        self._finish_job(job_id)
        return None

    def _finish_job(self, job_id: str) -> None:
        """Finalize one job and update dispatch counters once."""
        if job_id in self.active_jobs:
            self.active_jobs.remove(job_id)
            self.state.mark_run_complete()
        self.submitted_jobs.pop(job_id, None)
        self.completed_jobs.add(job_id)
