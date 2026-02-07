from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SnapshotRequest:
    repo_id: str
    commit: str


@dataclass(frozen=True)
class SnapshotResult:
    snapshot_id: str


def build_snapshot(request: SnapshotRequest) -> SnapshotResult:
    """Placeholder snapshot builder."""
    if not isinstance(request, SnapshotRequest):
        raise TypeError("request must be SnapshotRequest")
    snapshot_id = f"{request.repo_id}-{request.commit}"
    return SnapshotResult(snapshot_id=snapshot_id)

