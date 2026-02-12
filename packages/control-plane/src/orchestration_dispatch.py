from dataclasses import dataclass


@dataclass
class ConcurrencyLimits:
    max_active_runs: int
    active_runs: int = 0

    def can_dispatch(self) -> bool:
        return self.active_runs < self.max_active_runs


@dataclass(frozen=True)
class ScheduleDecision:
    run_id: str
    should_dispatch: bool


def decide(run_id: str, concurrency_limit: int) -> ScheduleDecision:
    """Return a scheduling decision for a run."""
    if not isinstance(run_id, str):
        raise TypeError("run_id must be str")
    if not isinstance(concurrency_limit, int):
        raise TypeError("concurrency_limit must be int")
    return ScheduleDecision(run_id=run_id, should_dispatch=True)


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


@dataclass(frozen=True)
class StopRequest:
    run_id: str


def stop_run(request: StopRequest) -> None:
    """Placeholder stop logic."""
    if not isinstance(request, StopRequest):
        raise TypeError("request must be StopRequest")
