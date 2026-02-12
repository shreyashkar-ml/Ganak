from dataclasses import dataclass, field
from datetime import datetime, timezone


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


@dataclass
class SnapshotCache:
    _cache: dict[str, str] = field(default_factory=dict)

    def get(self, key: str) -> str | None:
        if not isinstance(key, str):
            raise TypeError("key must be str")
        return self._cache.get(key)

    def set(self, key: str, snapshot_id: str) -> None:
        if not isinstance(key, str) or not isinstance(snapshot_id, str):
            raise TypeError("key and snapshot_id must be str")
        self._cache[key] = snapshot_id


def snapshot_name(repo_id: str, commit: str) -> str:
    """Generate a snapshot name from repo and commit."""
    if not isinstance(repo_id, str) or not isinstance(commit, str):
        raise TypeError("repo_id and commit must be str")
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{repo_id}-{commit}-{ts}"
