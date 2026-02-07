from __future__ import annotations

from typing import Iterable, Protocol


class StreamClient(Protocol):
    """Interface for streaming events from runner to control plane."""

    def send(self, events: Iterable[dict]) -> None:
        ...

