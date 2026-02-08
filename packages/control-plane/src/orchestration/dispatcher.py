from dataclasses import dataclass

from orchestration.limits import ConcurrencyLimits


@dataclass(frozen=True)
class DispatchRequest:
    run_id: str
    snapshot_id: str


def dispatch(request: DispatchRequest, limits: ConcurrencyLimits) -> bool:
    """Dispatch a run if within limits."""
    if not isinstance(request, DispatchRequest):
        raise TypeError("request must be DispatchRequest")
    if not isinstance(limits, ConcurrencyLimits):
        raise TypeError("limits must be ConcurrencyLimits")
    return limits.can_dispatch()