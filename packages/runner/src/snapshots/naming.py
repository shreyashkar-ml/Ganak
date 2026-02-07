from __future__ import annotations

from datetime import datetime, timezone


def snapshot_name(repo_id: str, commit: str) -> str:
    """Generate a snapshot name from repo and commit."""
    if not isinstance(repo_id, str) or not isinstance(commit, str):
        raise TypeError("repo_id and commit must be str")
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{repo_id}-{commit}-{ts}"

