from __future__ import annotations

from typing import Protocol


class StateBackend(Protocol):
    """Durable backend for session/run/event state."""

    def health(self) -> bool:
        ...

