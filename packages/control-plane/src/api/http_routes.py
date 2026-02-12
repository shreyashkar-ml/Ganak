import uuid
from typing import Mapping

from api.state import ControlPlaneState


def health_status() -> dict[str, str]:
    """Return control-plane health status."""
    return {"status": "ok"}


def login_status() -> dict[str, str]:
    """Return placeholder auth status."""
    return {"status": "not_configured"}


def handle_webhook(event: dict) -> None:
    """Validate webhook payload shape."""
    if not isinstance(event, dict):
        raise TypeError("event must be dict")


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


def list_artifacts(state: ControlPlaneState, run_id: str) -> list[Mapping[str, str]]:
    """Placeholder artifacts listing."""
    if not isinstance(state, ControlPlaneState):
        raise TypeError("state must be ControlPlaneState")
    if not isinstance(run_id, str):
        raise TypeError("run_id must be str")
    return []
