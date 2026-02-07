from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GitCommit:
    message: str
    author: str


def commit_changes(path: str, commit: GitCommit) -> None:
    """Placeholder commit operation."""
    if not isinstance(path, str):
        raise TypeError("path must be str")
    if not isinstance(commit, GitCommit):
        raise TypeError("commit must be GitCommit")

