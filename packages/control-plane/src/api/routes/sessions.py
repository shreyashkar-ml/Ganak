
import uuid
from typing import Mapping

from api.state import ControlPlaneState


def create_session(state: ControlPlaneState, repo_id: str) -> Mapping[str, str]:
    """Create a session in memory."""
    if not isinstance(state, ControlPlaneState):
        raise TypeError("state must be ControlPlaneState")
    if not isinstance(repo_id, str):
        raise TypeError("repo_id must be str")
    session_id = f"sess_{uuid.uuid4().hex}"
    session = {"id": session_id, "repo_id": repo_id, "status": "active"}
    state.sessions[session_id] = session
    return session
