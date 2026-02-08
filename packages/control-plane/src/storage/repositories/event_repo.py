
from dataclasses import dataclass, field
from typing import List

from storage.models.event import EventModel


@dataclass
class EventRepository:
    _store: List[EventModel] = field(default_factory=list)

    def add(self, event: EventModel) -> None:
        if not isinstance(event, EventModel):
            raise TypeError("event must be EventModel")
        self._store.append(event)

    def list_for_session(self, session_id: str) -> list[EventModel]:
        if not isinstance(session_id, str):
            raise TypeError("session_id must be str")
        return [event for event in self._store if event.session_id == session_id]

