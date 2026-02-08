"""Minimal control-plane skeleton connecting agent-core and runner."""

from dataclasses import dataclass, field
from typing import Any

from minimal_agent_core import EventLog, ScopePolicy, make_default_registry, make_event, new_id
from minimal_runner import LocalRunnerBackend, RunnerBackend, RunnerJob, RunnerStateInterface, SnapshotRequest, build_snapshot


@dataclass(frozen=True)
class SessionRecord:
    """Session model."""

    id: str
    repo_id: str
    status: str


@dataclass(frozen=True)
class RunRecord:
    """Run model."""

    id: str
    session_id: str
    prompt: str
    status: str


@dataclass
class PromptQueue:
    """Queue of run IDs."""

    items: list[str] = field(default_factory=list)

    def enqueue(self, run_id: str) -> None:
        """Push run to queue."""
        if not isinstance(run_id, str):
            raise TypeError("run_id must be str")
        self.items.append(run_id)

    def dequeue(self) -> str | None:
        """Pop next run from queue."""
        if not self.items:
            return None
        return self.items.pop(0)


@dataclass
class ConcurrencyLimits:
    """Dispatch concurrency controls."""

    max_active_runs: int
    active_runs: int = 0

    def can_dispatch(self) -> bool:
        """Return whether dispatch can happen now."""
        return self.active_runs < self.max_active_runs

    def mark_dispatched(self) -> None:
        """Increment active run count."""
        self.active_runs += 1

    def mark_finished(self) -> None:
        """Decrement active run count."""
        self.active_runs = max(0, self.active_runs - 1)


@dataclass
class ControlPlaneState(RunnerStateInterface):
    """Control-plane state."""

    sessions: dict[str, SessionRecord] = field(default_factory=dict)
    runs: dict[str, RunRecord] = field(default_factory=dict)
    event_log: EventLog = field(default_factory=EventLog)
    queue: PromptQueue = field(default_factory=PromptQueue)
    limits: ConcurrencyLimits = field(default_factory=lambda: ConcurrencyLimits(max_active_runs=2))
    run_to_job: dict[str, str] = field(default_factory=dict)

    def get_run(self, run_id: str) -> RunRecord:
        """Get run by ID."""
        if not isinstance(run_id, str):
            raise TypeError("run_id must be str")
        if run_id not in self.runs:
            raise KeyError(f"unknown run: {run_id}")
        return self.runs[run_id]

    def update_run_status(self, run_id: str, status: str) -> None:
        """Update run status using explicit RunRecord reconstruction."""
        if not isinstance(status, str):
            raise TypeError("status must be str")
        run = self.get_run(run_id)
        self.runs[run_id] = RunRecord(
            id=run.id,
            session_id=run.session_id,
            prompt=run.prompt,
            status=status,
        )

    def mark_run_complete(self) -> None:
        """Update dispatch counters when one run completes."""
        self.limits.mark_finished()

    def append_event(self, event_type: str, session_id: str, run_id: str, payload: dict[str, Any]) -> None:
        """Append one event using envelope helper."""
        self.event_log.append(make_event(event_type, session_id, run_id, payload))

    def get_event_log(self) -> EventLog:
        """Expose event log for agent execution path."""
        return self.event_log


@dataclass
class ControlPlane:
    """Control-plane orchestration."""

    state: ControlPlaneState
    runner: RunnerBackend

    def create_session(self, repo_id: str) -> SessionRecord:
        """Create active session."""
        if not isinstance(repo_id, str):
            raise TypeError("repo_id must be str")
        session = SessionRecord(id=new_id("sess"), repo_id=repo_id, status="active")
        self.state.sessions[session.id] = session
        return session

    def create_run(self, session_id: str, prompt: str) -> RunRecord:
        """Create queued run and emit queue event."""
        if session_id not in self.state.sessions:
            raise KeyError(f"unknown session: {session_id}")
        run = RunRecord(id=new_id("run"), session_id=session_id, prompt=prompt, status="queued")
        self.state.runs[run.id] = run
        self.state.event_log.append(make_event("run_queued", session_id, run.id, {"prompt": prompt}))
        self.state.queue.enqueue(run.id)
        return run

    def process_once(self) -> bool:
        """Dispatch one queued run."""
        run_id = self.state.queue.dequeue()
        if run_id is None:
            return False
        if not self.state.limits.can_dispatch():
            run = self.state.runs[run_id]
            self.state.queue.enqueue(run_id)
            self.state.event_log.append(
                make_event(
                    "run_dispatch_blocked",
                    run.session_id,
                    run.id,
                    {"active_runs": self.state.limits.active_runs, "max_active_runs": self.state.limits.max_active_runs},
                )
            )
            return False
        run = self.state.get_run(run_id)
        self.state.update_run_status(run_id, "dispatched")
        self.state.limits.mark_dispatched()
        self.state.event_log.append(make_event("run_dispatched", run.session_id, run.id, {}))
        snapshot = build_snapshot(SnapshotRequest(repo_id=self.state.sessions[run.session_id].repo_id, commit="HEAD"))
        job = RunnerJob(job_id=new_id("job"), session_id=run.session_id, run_id=run.id, snapshot_id=snapshot.snapshot_id)
        self.state.run_to_job[run.id] = job.job_id
        self.runner.submit_job(job)
        return True

    def stream_events(self, session_id: str) -> list[dict[str, Any]]:
        """Return events for one session."""
        return self.state.event_log.list_for_session(session_id)

    def cancel_run(self, run_id: str) -> bool:
        """Request cancellation for a run via its current runner job."""
        if run_id not in self.state.run_to_job:
            return False
        self.runner.cancel_job(self.state.run_to_job[run_id])
        return True


def demo() -> None:
    """Run one complete minimal skeleton flow."""
    state = ControlPlaneState()
    registry = make_default_registry()
    scope_policy = ScopePolicy(allowed={"repo.read", "git.write"})
    runner = LocalRunnerBackend(state=state, tool_registry=registry, scope_policy=scope_policy)
    control_plane = ControlPlane(state=state, runner=runner)

    session = control_plane.create_session(repo_id="ganak_repo_demo")
    run = control_plane.create_run(session_id=session.id, prompt="Fix failing test and open PR")
    control_plane.process_once()

    print(f"session={session.id} run={run.id}")
    for event in control_plane.stream_events(session.id):
        print(f"{event['type']}: {event['payload']}")


if __name__ == "__main__":
    demo()
