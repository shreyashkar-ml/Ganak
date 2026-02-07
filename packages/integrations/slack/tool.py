from __future__ import annotations


def send_message(channel: str, text: str) -> bool:
    """Placeholder Slack message send."""
    if not isinstance(channel, str) or not isinstance(text, str):
        raise TypeError("channel and text must be str")
    return True

