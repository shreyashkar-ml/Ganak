from __future__ import annotations


def sync_repo(path: str) -> None:
    """Placeholder repo sync."""
    if not isinstance(path, str):
        raise TypeError("path must be str")

