
from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    value: str
    scopes: list[str]

