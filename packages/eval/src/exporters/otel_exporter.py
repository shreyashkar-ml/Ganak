from __future__ import annotations

from typing import Mapping


def export_metrics(metrics: Mapping[str, object]) -> None:
    if not isinstance(metrics, Mapping):
        raise TypeError("metrics must be mapping")

