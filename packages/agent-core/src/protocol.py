import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping


def utc_now_iso() -> str:
    """Return an ISO8601 timestamp in UTC."""
    return datetime.now(timezone.utc).isoformat()


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


def _event_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


def event_run_started(session_id: str, run_id: str, prompt: str) -> Mapping[str, object]:
    return EventEnvelope(
        id=_event_id("evt"),
        ts=utc_now_iso(),
        type="run_started",
        session_id=session_id,
        run_id=run_id,
        payload={"prompt": prompt},
    ).to_dict()


def event_step_started(session_id: str, run_id: str, description: str) -> Mapping[str, object]:
    return EventEnvelope(
        id=_event_id("evt"),
        ts=utc_now_iso(),
        type="step_started",
        session_id=session_id,
        run_id=run_id,
        payload={"description": description},
    ).to_dict()


def event_step_finished(session_id: str, run_id: str, description: str) -> Mapping[str, object]:
    return EventEnvelope(
        id=_event_id("evt"),
        ts=utc_now_iso(),
        type="step_finished",
        session_id=session_id,
        run_id=run_id,
        payload={"description": description},
    ).to_dict()


def event_run_finished(session_id: str, run_id: str, stopped: bool) -> Mapping[str, object]:
    return EventEnvelope(
        id=_event_id("evt"),
        ts=utc_now_iso(),
        type="run_finished",
        session_id=session_id,
        run_id=run_id,
        payload={"stopped": stopped},
    ).to_dict()


def serialize_event(event: Mapping[str, Any]) -> str:
    if not isinstance(event, Mapping):
        raise TypeError("event must be a mapping")
    return json.dumps(event, separators=(",", ":"))


def deserialize_event(data: str) -> Mapping[str, Any]:
    if not isinstance(data, str):
        raise TypeError("data must be str")
    return json.loads(data)
