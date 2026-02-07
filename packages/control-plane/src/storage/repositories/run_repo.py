from __future__ import annotations

from dataclasses import dataclass, field

from storage.models.run import RunModel


@dataclass
class RunRepository:
    _store: dict[str, RunModel] = field(default_factory=dict)

    def add(self, run: RunModel) -> None:
        if not isinstance(run, RunModel):
            raise TypeError("run must be RunModel")
        self._store[run.id] = run

    def get(self, run_id: str) -> RunModel | None:
        if not isinstance(run_id, str):
            raise TypeError("run_id must be str")
        return self._store.get(run_id)

