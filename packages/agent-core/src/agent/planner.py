from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class PlanStep:
    description: str
    tool_name: str | None = None
    tool_input: dict | None = None


def plan_from_prompt(prompt: str) -> Iterable[PlanStep]:
    """Create a minimal plan from a prompt.

    This is a placeholder planner until a richer planner is wired in.
    """
    if not isinstance(prompt, str):
        raise TypeError("prompt must be str")
    if not prompt.strip():
        return []
    return [PlanStep(description=prompt)]

