from dataclasses import dataclass


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