from __future__ import annotations

from typing import Mapping

from api.state import ControlPlaneState


def stream_events(state: ControlPlaneState, session_id: str) -> Mapping[str, object]:
    """Return events for a session (stub stream)."""
    if not isinstance(state, ControlPlaneState):
        raise TypeError("state must be ControlPlaneState")
    if not isinstance(session_id, str):
        raise TypeError("session_id must be str")
    events = [event for event in state.events if event.get("session_id") == session_id]
    return {"session_id": session_id, "events": events}
