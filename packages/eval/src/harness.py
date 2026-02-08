
from typing import Iterable, Mapping

from metrics import score_run


def evaluate(events: Iterable[Mapping[str, object]]) -> dict[str, float]:
    """Evaluate a run from its events."""
    return {"score": score_run(events)}

