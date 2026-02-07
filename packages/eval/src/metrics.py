from __future__ import annotations

from typing import Iterable, Mapping


def score_run(events: Iterable[Mapping[str, object]]) -> float:
    """Score a run by counting successful tool results."""
    success = 0
    total = 0
    for event in events:
        if event.get("type") == "tool_result":
            total += 1
            if event.get("payload", {}).get("success") is True:
                success += 1
    if total == 0:
        return 0.0
    return success / total

