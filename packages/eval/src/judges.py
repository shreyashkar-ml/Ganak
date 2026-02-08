
from typing import Mapping


def rule_based_judge(result: Mapping[str, object]) -> str:
    """Return a verdict for a result payload."""
    score = result.get("score", 0.0)
    if not isinstance(score, (int, float)):
        raise TypeError("score must be number")
    return "pass" if score >= 0.8 else "fail"

