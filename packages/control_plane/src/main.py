import uuid
from dataclasses import dataclass, field
from typing import Mapping

from shared_models import RunRecord, SessionRecord


@dataclass
class PromptQueue:
    items: list[str] = field(default_factory=list)

    def enqueue(self, run_id: str) -> None:
        if not isinstance(run_id, str):
            raise TypeError("run_id must be str")
        self.items.append(run_id)

    def dequeue(self) -> str | None:
        if not self.items:
            return None
        return self.items.pop(0)


@dataclass
class ConcurrencyLimits:
    max_active_runs: int
    active_runs: int = 0

    def can_dispatch(self) -> bool:
        return self.active_runs < self.max_active_runs

    def mark_dispatched(self) -> None:
        self.active_runs += 1

    def mark_finished(self) -> None:
        self.active_runs = max(0, self.active_runs - 1)


@dataclass
class ControlPlaneState:
    sessions: dict[str, SessionRecord] = field(default_factory=dict)
    runs: dict[str, RunRecord] = field(default_factory=dict)
    events: list[Mapping[str, object]] = field(default_factory=list)
    repos: dict[str, Mapping[str, str]] = field(default_factory=dict)
    prompt_queue: PromptQueue = field(default_factory=PromptQueue)
    limits: ConcurrencyLimits = field(default_factory=lambda: ConcurrencyLimits(max_active_runs=2))

    def get_run(self, run_id: str) -> RunRecord:
        if not isinstance(run_id, str):
            raise TypeError("run_id must be str")
        if run_id not in self.runs:
            raise KeyError(f"unknown run: {run_id}")
        return self.runs[run_id]
    
    def update_run_status(self, run_id: str, new_status: str) -> None:
        if not isinstance(run_id, str):
            raise TypeError("run_id must be str")
        if not isinstance(new_status, str):
            raise TypeError("new_status must be str")
        run = self.get_run(run_id)
        self.runs[run_id] = RunRecord(
            id=run.id, 
            session_id=run.session_id, 
            prompt=run.prompt,
            status=new_status
        )

    def mark_run_complete(self) -> None:
        self.limits.mark_finished()

@dataclass
class ControlPlane:
    state: ControlPlaneState

    def health_status(self) -> dict[str, str]:
        return {"status": "ok"}

    def create_session(self, repo_id: str) -> Mapping[str, str]:
        if not isinstance(repo_id, str):
            raise TypeError("repo_id must be str")
        session_id = f"sess_{uuid.uuid4().hex}"
        session = SessionRecord(id=session_id, repo_id=repo_id, status="active")
        self.state.sessions[session_id] = session
        return {"id": session.id, "repo_id": session.repo_id, "status": session.status}

    def create_run(self, session_id: str, prompt: str) -> Mapping[str, str]:
        if not isinstance(session_id, str):
            raise TypeError("session_id must be str")
        if not isinstance(prompt, str):
            raise TypeError("prompt must be str")
        if session_id not in self.state.sessions:
            raise KeyError(f"unknown session: {session_id}")
        run_id = f"run_{uuid.uuid4().hex}"
        run = RunRecord(id=run_id, session_id=session_id, prompt=prompt, status="queued")
        self.state.runs[run_id] = run
        self.state.prompt_queue.enqueue(run_id)
        self.state.events.append(self._make_event("run_queued", session_id, run_id, {"prompt": prompt}))
        return {"id": run.id, "session_id": run.session_id, "status": run.status}

    def process_queue(self) -> bool:
        """Dispatch one run from the queue if concurrency limits allow."""

    def create_repo(self, url: str) -> Mapping[str, str]:
        if not isinstance(url, str):
            raise TypeError("url must be str")
        repo_id = f"repo_{uuid.uuid4().hex}"
        repo = {"id": repo_id, "url": url}
        self.state.repos[repo_id] = repo
        return repo

    def list_artifacts(self, run_id: str) -> list[Mapping[str, str]]:
        if not isinstance(run_id, str):
            raise TypeError("run_id must be str")
        return []

    def stream_events(self, session_id: str) -> Mapping[str, object]:
        if not isinstance(session_id, str):
            raise TypeError("session_id must be str")
        events = [event for event in self.state.events if event.get("session_id") == session_id]
        return {"session_id": session_id, "events": events}

    def _make_event(self, event_type: str, session_id: str, run_id: str, payload: Mapping[str, object]) -> Mapping[str, object]:
        return {
            "id": f"evt_{uuid.uuid4().hex}",
            "type": event_type,
            "session_id": session_id,
            "run_id": run_id,
            "payload": dict(payload),
        }
