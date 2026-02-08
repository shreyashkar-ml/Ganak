
from dataclasses import dataclass, field

from storage.models.session import SessionModel


@dataclass
class SessionRepository:
    _store: dict[str, SessionModel] = field(default_factory=dict)

    def add(self, session: SessionModel) -> None:
        if not isinstance(session, SessionModel):
            raise TypeError("session must be SessionModel")
        self._store[session.id] = session

    def get(self, session_id: str) -> SessionModel | None:
        if not isinstance(session_id, str):
            raise TypeError("session_id must be str")
        return self._store.get(session_id)

