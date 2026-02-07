from __future__ import annotations

import uuid
from typing import Mapping

from api.state import ControlPlaneState


def create_run(state: ControlPlaneState, session_id: str, prompt: str) -> Mapping[str, str]:
    """Create a run and append a run_started event."""
    if not isinstance(state, ControlPlaneState):
        raise TypeError("state must be ControlPlaneState")
    if not isinstance(session_id, str):
        raise TypeError("session_id must be str")
    if not isinstance(prompt, str):
        raise TypeError("prompt must be str")
    run_id = f"run_{uuid.uuid4().hex}"
    run = {"id": run_id, "session_id": session_id, "status": "queued"}
    state.runs[run_id] = run
    state.events.append(
        {
            "id": f"evt_{uuid.uuid4().hex}",
            "type": "run_started",
            "session_id": session_id,
            "run_id": run_id,
            "payload": {"prompt": prompt},
        }
    )
    return run
