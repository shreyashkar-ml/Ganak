
from dataclasses import dataclass


@dataclass(frozen=True)
class RunPolicy:
    max_steps: int = 8

