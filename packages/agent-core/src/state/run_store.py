from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class RunRecord:
    run_id: str
    session_id: str
    status: str


@dataclass
class RunStore:
    _runs: Dict[str, RunRecord] = field(default_factory=dict)

    def create(self, run: RunRecord) -> None:
        """Create a run record."""
        if not isinstance(run, RunRecord):
            raise TypeError("run must be RunRecord")
        if run.run_id in self._runs:
            raise ValueError(f"run exists: {run.run_id}")
        self._runs[run.run_id] = run

    def get(self, run_id: str) -> RunRecord:
        """Get a run record by id."""
        if not isinstance(run_id, str):
            raise TypeError("run_id must be str")
        if run_id not in self._runs:
            raise KeyError(f"run not found: {run_id}")
        return self._runs[run_id]

    def update_status(self, run_id: str, status: str) -> None:
        """Update run status."""
        if not isinstance(status, str):
            raise TypeError("status must be str")
        record = self.get(run_id)
        self._runs[run_id] = RunRecord(run_id=record.run_id, session_id=record.session_id, status=status)

