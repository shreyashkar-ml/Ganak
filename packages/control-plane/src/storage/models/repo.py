from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RepoModel:
    id: str
    url: str

