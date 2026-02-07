from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Org:
    id: str
    name: str

