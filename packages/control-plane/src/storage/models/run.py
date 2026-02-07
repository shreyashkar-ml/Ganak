from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RunModel:
    id: str
    session_id: str
    status: str

