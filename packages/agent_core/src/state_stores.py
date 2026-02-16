from dataclasses import dataclass, field
from typing import Dict

from shared_models import EventLog, RunRecord, SessionRecord


@dataclass
class RunStore:
    _runs: Dict[str, RunRecord] = field(default_factory=dict)

    def create(self, run: RunRecord) -> None:
        """Create a run record."""
        if not isinstance(run, RunRecord):
            raise TypeError("run must be RunRecord")
        if run.id in self._runs:
            raise ValueError(f"run exists: {run.id}")
        self._runs[run.id] = run

    def get(self, run_id: str) -> RunRecord:
        """Get a run record by id."""
        if not isinstance(run_id, str):
            raise TypeError("run_id must be str")
        if run_id not in self._runs:
            raise KeyError(f"run not found: {run_id}")
        return self._runs[run_id]

    def update_status(self, run_id: str, status: str) -> None:
        """Update run status."""
        if not isinstance(status, str):
            raise TypeError("status must be str")
        record = self.get(run_id)
        self._runs[run_id] = RunRecord(
            id=record.id,
            session_id=record.session_id,
            prompt=record.prompt,
            status=status,
        )


@dataclass
class SessionStore:
    _sessions: Dict[str, SessionRecord] = field(default_factory=dict)

    def create(self, session: SessionRecord) -> None:
        """Create a session record."""
        if not isinstance(session, SessionRecord):
            raise TypeError("session must be SessionRecord")
        if session.id in self._sessions:
            raise ValueError(f"session exists: {session.id}")
        self._sessions[session.id] = session

    def get(self, session_id: str) -> SessionRecord:
        """Get a session record by id."""
        if not isinstance(session_id, str):
            raise TypeError("session_id must be str")
        if session_id not in self._sessions:
            raise KeyError(f"session not found: {session_id}")
        return self._sessions[session_id]

    def update_status(self, session_id: str, status: str) -> None:
        """Update session status."""
        if not isinstance(status, str):
            raise TypeError("status must be str")
        record = self.get(session_id)
        self._sessions[session_id] = SessionRecord(
            id=record.id,
            repo_id=record.repo_id,
            status=status,
        )
