from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class EventEnvelope:
    id: str
    ts: str
    type: str
    session_id: str
    run_id: str
    payload: Mapping[str, Any]

    def to_dict(self) -> Mapping[str, Any]:
        return {
            "id": self.id,
            "ts": self.ts,
            "type": self.type,
            "session_id": self.session_id,
            "run_id": self.run_id,
            "payload": dict(self.payload),
        }


@dataclass(frozen=True)
class RunnerJob:
    job_id: str
    session_id: str
    run_id: str
    snapshot_id: str


@dataclass(frozen=True)
class SnapshotRequest:
    repo_id: str
    commit: str


@dataclass(frozen=True)
class SnapshotResult:
    snapshot_id: str


@dataclass(frozen=True)
class ToolContract:
    name: str
    input_schema: Mapping[str, Any]
    output_schema: Mapping[str, Any]
    scopes: list[str]


@dataclass(frozen=True)
class SessionRecord:
    id: str
    repo_id: str
    status: str


@dataclass(frozen=True)
class RunRecord:
    id: str
    session_id: str
    prompt: str = ""
    status: str = "queued"


@dataclass
class EventLog:
    _events: list[Mapping[str, object]] = field(default_factory=list)

    def append(self, event: Mapping[str, object]) -> None:
        if not isinstance(event, Mapping):
            raise TypeError("event must be a mapping")
        self._events.append(event)

    def list(self) -> Iterable[Mapping[str, object]]:
        return list(self._events)
