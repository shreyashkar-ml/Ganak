from __future__ import annotations

from typing import Iterable, Mapping


def replay_events(events: Iterable[Mapping[str, object]]) -> list[Mapping[str, object]]:
    """Replay events into a list for analysis."""
    return list(events)

