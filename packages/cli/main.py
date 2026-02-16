import argparse
import json
import urllib.request
from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class CliConfig:
    api_base: str = "http://localhost:8000"


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


def format_events(events: Iterable[Mapping[str, object]]) -> str:
    lines = []
    for event in events:
        lines.append(f"{event.get('type', '')}: {event.get('id', '')}")
    return "\n".join(lines)


def run_login() -> None:
    print("Login not configured")


def register_repo(client: ApiClient, url: str) -> None:
    repo = client.register_repo(url)
    print(repo)


def create_run(client: ApiClient, session_id: str, prompt: str) -> None:
    run = client.create_run(session_id, prompt)
    print(run)


def create_session(client: ApiClient, repo_id: str) -> None:
    session = client.create_session(repo_id)
    print(session)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bg-agent")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("login")

    session_parser = sub.add_parser("session")
    session_parser.add_argument("repo_id")

    run_parser = sub.add_parser("run")
    run_parser.add_argument("session_id")
    run_parser.add_argument("prompt")

    repo_parser = sub.add_parser("repo")
    repo_parser.add_argument("url")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    client = ApiClient(CliConfig())

    if args.command == "login":
        run_login()
        return
    if args.command == "session":
        create_session(client, args.repo_id)
        return
    if args.command == "run":
        create_run(client, args.session_id, args.prompt)
        return
    if args.command == "repo":
        register_repo(client, args.url)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
