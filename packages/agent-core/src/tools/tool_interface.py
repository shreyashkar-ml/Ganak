from dataclasses import dataclass
from typing import Any, Callable, Mapping

ToolHandler = Callable[[Mapping[str, Any]], Mapping[str, Any]]


@dataclass(frozen=True)
class ToolSpec:
    name: str
    input_schema: Mapping[str, Any]
    output_schema: Mapping[str, Any]
    scopes: list[str]


@dataclass
class Tool:
    spec: ToolSpec
    handler: ToolHandler

    def run(self, payload: Mapping[str, Any]) -> Mapping[str, Any]:
        """Run tool handler with validated input payload."""
        if not isinstance(payload, Mapping):
            raise TypeError("payload must be a mapping")
        return self.handler(payload)