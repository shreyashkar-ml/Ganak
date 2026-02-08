
from dataclasses import dataclass


@dataclass(frozen=True)
class EgressPolicy:
    allow_internet: bool
    allowlist: list[str]

