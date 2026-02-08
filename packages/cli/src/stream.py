
from typing import Iterable, Mapping


def format_events(events: Iterable[Mapping[str, object]]) -> str:
    lines = []
    for event in events:
        lines.append(f"{event.get('type', '')}: {event.get('id', '')}")
    return "\n".join(lines)

