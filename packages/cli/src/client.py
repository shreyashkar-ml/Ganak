
import json
import urllib.request
from dataclasses import dataclass
from typing import Mapping

from config import CliConfig


@dataclass
class ApiClient:
    config: CliConfig

    def _request(self, method: str, path: str, payload: Mapping[str, object] | None = None) -> Mapping[str, object]:
        if not isinstance(method, str) or not isinstance(path, str):
            raise TypeError("method and path must be str")
        url = f"{self.config.api_base}{path}"
        data = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def create_session(self, repo_id: str) -> Mapping[str, object]:
        return self._request("POST", "/sessions", {"repo_id": repo_id})

    def create_run(self, session_id: str, prompt: str) -> Mapping[str, object]:
        return self._request("POST", "/runs", {"session_id": session_id, "prompt": prompt})

    def register_repo(self, url: str) -> Mapping[str, object]:
        return self._request("POST", "/repos", {"url": url})

    def list_events(self, session_id: str) -> Mapping[str, object]:
        return self._request("GET", f"/events/{session_id}")

