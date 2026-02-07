from __future__ import annotations

from typing import Callable, Mapping, Any

ToolHandler = Callable[[Mapping[str, Any]], Mapping[str, Any]]


def with_logging(handler: ToolHandler, name: str) -> ToolHandler:
    """Wrap a tool handler to emit a simple log payload."""
    def wrapped(payload: Mapping[str, Any]) -> Mapping[str, Any]:
        if not isinstance(payload, Mapping):
            raise TypeError("payload must be a mapping")
        result = handler(payload)
        return {"tool": name, "result": result}

    return wrapped

