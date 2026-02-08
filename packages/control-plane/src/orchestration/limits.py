
from dataclasses import dataclass


@dataclass
class ConcurrencyLimits:
    max_active_runs: int
    active_runs: int = 0

    def can_dispatch(self) -> bool:
        return self.active_runs < self.max_active_runs

