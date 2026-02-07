from __future__ import annotations


def handle_webhook(event: dict) -> None:
    if not isinstance(event, dict):
        raise TypeError("event must be dict")

