
from dataclasses import dataclass, field


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

