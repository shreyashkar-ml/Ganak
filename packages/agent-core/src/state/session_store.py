from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class SessionRecord:
    session_id: str
    repo_id: str
    status: str


@dataclass
class SessionStore:
    _sessions: Dict[str, SessionRecord] = field(default_factory=dict)

    def create(self, session: SessionRecord) -> None:
        """Create a session record."""
        if not isinstance(session, SessionRecord):
            raise TypeError("session must be SessionRecord")
        if session.session_id in self._sessions:
            raise ValueError(f"session exists: {session.session_id}")
        self._sessions[session.session_id] = session

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
            session_id=record.session_id,
            repo_id=record.repo_id,
            status=status,
        )

