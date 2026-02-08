
from dataclasses import dataclass, field
from typing import Iterable, Mapping


@dataclass
class EventLog:
    _events: list[Mapping[str, object]] = field(default_factory=list)

    def append(self, event: Mapping[str, object]) -> None:
        """Append a serialized event to the log."""
        if not isinstance(event, Mapping):
            raise TypeError("event must be a mapping")
        self._events.append(event)

    def list(self) -> Iterable[Mapping[str, object]]:
        return list(self._events)

