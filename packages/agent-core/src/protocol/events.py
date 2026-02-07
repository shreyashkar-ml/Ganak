from __future__ import annotations

import uuid
from typing import Mapping

from protocol.envelope import EventEnvelope, utc_now_iso


def _event_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


def event_run_started(session_id: str, run_id: str, prompt: str) -> Mapping[str, object]:
    """Create a run_started event."""
    return EventEnvelope(
        id=_event_id("evt"),
        ts=utc_now_iso(),
        type="run_started",
        session_id=session_id,
        run_id=run_id,
        payload={"prompt": prompt},
    ).to_dict()


def event_step_started(session_id: str, run_id: str, description: str) -> Mapping[str, object]:
    """Create a step_started event."""
    return EventEnvelope(
        id=_event_id("evt"),
        ts=utc_now_iso(),
        type="step_started",
        session_id=session_id,
        run_id=run_id,
        payload={"description": description},
    ).to_dict()


def event_step_finished(session_id: str, run_id: str, description: str) -> Mapping[str, object]:
    """Create a step_finished event."""
    return EventEnvelope(
        id=_event_id("evt"),
        ts=utc_now_iso(),
        type="step_finished",
        session_id=session_id,
        run_id=run_id,
        payload={"description": description},
    ).to_dict()


def event_run_finished(session_id: str, run_id: str, stopped: bool) -> Mapping[str, object]:
    """Create a run_finished event."""
    return EventEnvelope(
        id=_event_id("evt"),
        ts=utc_now_iso(),
        type="run_finished",
        session_id=session_id,
        run_id=run_id,
        payload={"stopped": stopped},
    ).to_dict()
