from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StopRequest:
    run_id: str


def stop_run(request: StopRequest) -> None:
    """Placeholder stop logic."""
    if not isinstance(request, StopRequest):
        raise TypeError("request must be StopRequest")

