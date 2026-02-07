from __future__ import annotations

from client import ApiClient


def create_session(client: ApiClient, repo_id: str) -> None:
    session = client.create_session(repo_id)
    print(session)

