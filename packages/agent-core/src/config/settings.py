from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentSettings:
    max_steps: int = 8
    enable_verification: bool = True

