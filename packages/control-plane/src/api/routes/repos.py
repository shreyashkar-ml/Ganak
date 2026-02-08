
import uuid
from typing import Mapping

from api.state import ControlPlaneState


def create_repo(state: ControlPlaneState, url: str) -> Mapping[str, str]:
    """Register a repo in memory."""
    if not isinstance(state, ControlPlaneState):
        raise TypeError("state must be ControlPlaneState")
    if not isinstance(url, str):
        raise TypeError("url must be str")
    repo_id = f"repo_{uuid.uuid4().hex}"
    repo = {"id": repo_id, "url": url}
    state.repos[repo_id] = repo
    return repo
