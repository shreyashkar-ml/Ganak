import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel

# Ensure `api.*` imports resolve when launched from repository root.
_SRC_ROOT = Path(__file__).resolve().parents[1]
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from api.http_routes import create_repo, create_run, create_session, health_status
from api.state import ControlPlaneState
from api.ws_stream import stream_events


@dataclass(frozen=True)
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    limit_concurrency: int = 200
    backlog: int = 2048
    keepalive_timeout_s: int = 5
    state_backend: str = "memory"


class SessionCreateRequest(BaseModel):
    repo_id: str


class RunCreateRequest(BaseModel):
    session_id: str
    prompt: str


class RepoCreateRequest(BaseModel):
    url: str


def load_server_config() -> ServerConfig:
    """Load runtime configuration from environment."""
    return ServerConfig(
        host=os.getenv("CONTROL_PLANE_HOST", "0.0.0.0"),
        port=int(os.getenv("CONTROL_PLANE_PORT", "8000")),
        workers=int(os.getenv("CONTROL_PLANE_WORKERS", "1")),
        limit_concurrency=int(os.getenv("CONTROL_PLANE_LIMIT_CONCURRENCY", "200")),
        backlog=int(os.getenv("CONTROL_PLANE_BACKLOG", "2048")),
        keepalive_timeout_s=int(os.getenv("CONTROL_PLANE_KEEPALIVE_TIMEOUT", "5")),
        state_backend=os.getenv("CONTROL_PLANE_STATE_BACKEND", "memory"),
    )


def validate_server_config(config: ServerConfig) -> None:
    """Prevent unsafe scale-out for in-memory state mode."""
    if config.state_backend == "memory" and config.workers > 1:
        raise ValueError(
            "CONTROL_PLANE_WORKERS > 1 requires a durable shared state backend. "
            "Set CONTROL_PLANE_STATE_BACKEND to a non-memory backend before scaling workers."
        )


app = FastAPI(title="Ganak Control Plane", version="0.1.0")
app.state.control_plane_state = ControlPlaneState()


def _state(request: Request) -> ControlPlaneState:
    state = request.app.state.control_plane_state
    if not isinstance(state, ControlPlaneState):
        raise TypeError("app.state.control_plane_state must be ControlPlaneState")
    return state


@app.get("/health")
def get_health() -> dict[str, str]:
    return health_status()


@app.post("/sessions")
def post_session(payload: SessionCreateRequest, request: Request) -> Mapping[str, str]:
    return create_session(_state(request), payload.repo_id)


@app.post("/runs")
def post_run(payload: RunCreateRequest, request: Request) -> Mapping[str, str]:
    return create_run(_state(request), payload.session_id, payload.prompt)


@app.post("/repos")
def post_repo(payload: RepoCreateRequest, request: Request) -> Mapping[str, str]:
    return create_repo(_state(request), payload.url)


@app.get("/events/{session_id}")
def get_events(session_id: str, request: Request) -> Mapping[str, object]:
    return stream_events(_state(request), session_id)


def serve() -> None:
    """Run the control-plane API with production-friendly server options."""
    config = load_server_config()
    validate_server_config(config)
    uvicorn.run(
        "api.app:app",
        app_dir=str(_SRC_ROOT),
        host=config.host,
        port=config.port,
        workers=config.workers,
        limit_concurrency=config.limit_concurrency,
        backlog=config.backlog,
        timeout_keep_alive=config.keepalive_timeout_s,
    )


if __name__ == "__main__":
    serve()
