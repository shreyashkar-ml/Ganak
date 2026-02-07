from __future__ import annotations

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

