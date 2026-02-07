from __future__ import annotations


def send_metric(name: str, value: float) -> None:
    if not isinstance(name, str) or not isinstance(value, (int, float)):
        raise TypeError("name must be str and value must be number")

