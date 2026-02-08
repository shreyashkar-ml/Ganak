
import json
from typing import Any, Mapping


def serialize_event(event: Mapping[str, Any]) -> str:
    """Serialize an event mapping to JSON."""
    if not isinstance(event, Mapping):
        raise TypeError("event must be a mapping")
    return json.dumps(event, separators=(",", ":"))


def deserialize_event(data: str) -> Mapping[str, Any]:
    """Deserialize an event JSON string into a mapping."""
    if not isinstance(data, str):
        raise TypeError("data must be str")
    return json.loads(data)

