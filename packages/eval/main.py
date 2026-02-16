from typing import Iterable, Mapping


def replay_events(events: Iterable[Mapping[str, object]]) -> list[Mapping[str, object]]:
    return list(events)


def score_run(events: Iterable[Mapping[str, object]]) -> float:
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


def evaluate(events: Iterable[Mapping[str, object]]) -> dict[str, float]:
    return {"score": score_run(events)}


def rule_based_judge(result: Mapping[str, object]) -> str:
    score = result.get("score", 0.0)
    if not isinstance(score, (int, float)):
        raise TypeError("score must be number")
    return "pass" if score >= 0.8 else "fail"


def export_langfuse_metrics(metrics: Mapping[str, object]) -> None:
    if not isinstance(metrics, Mapping):
        raise TypeError("metrics must be mapping")


def export_otel_metrics(metrics: Mapping[str, object]) -> None:
    if not isinstance(metrics, Mapping):
        raise TypeError("metrics must be mapping")
