from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PullRequest:
    title: str
    body: str
    head: str
    base: str


def create_pull_request(pr: PullRequest) -> str:
    """Placeholder PR creation."""
    if not isinstance(pr, PullRequest):
        raise TypeError("pr must be PullRequest")
    return "https://github.com/example/repo/pull/1"

