from __future__ import annotations


def log_event(message: str) -> None:
    if not isinstance(message, str):
        raise TypeError("message must be str")

