from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Mapping

from api.routes.health import health_status
from api.routes.repos import create_repo
from api.routes.runs import create_run
from api.routes.sessions import create_session
from api.state import ControlPlaneState
from api.ws.stream import stream_events


class ControlPlaneHandler(BaseHTTPRequestHandler):
    state: ControlPlaneState

    def _read_json(self) -> Mapping[str, object]:
        length = int(self.headers.get("Content-Length", "0"))
        data = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            parsed = json.loads(data)
        except json.JSONDecodeError:
            parsed = {}
        if not isinstance(parsed, dict):
            return {}
        return parsed

    def _write_json(self, status: int, payload: Mapping[str, object]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._write_json(200, health_status())
            return
        if self.path.startswith("/events/"):
            session_id = self.path.split("/")[-1]
            payload = stream_events(self.state, session_id)
            self._write_json(200, payload)
            return
        self._write_json(404, {"error": "not_found"})

    def do_POST(self) -> None:
        if self.path == "/sessions":
            payload = self._read_json()
            session = create_session(self.state, payload.get("repo_id", "repo"))
            self._write_json(200, session)
            return
        if self.path == "/runs":
            payload = self._read_json()
            run = create_run(
                self.state,
                payload.get("session_id", ""),
                payload.get("prompt", ""),
            )
            self._write_json(200, run)
            return
        if self.path == "/repos":
            payload = self._read_json()
            repo = create_repo(self.state, payload.get("url", ""))
            self._write_json(200, repo)
            return
        self._write_json(404, {"error": "not_found"})


def _make_handler(state: ControlPlaneState):
    class BoundHandler(ControlPlaneHandler):
        pass

    BoundHandler.state = state
    return BoundHandler


def serve(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Run a minimal control-plane HTTP server."""
    state = ControlPlaneState()
    server = HTTPServer((host, port), _make_handler(state))
    server.serve_forever()


if __name__ == "__main__":
    serve()
