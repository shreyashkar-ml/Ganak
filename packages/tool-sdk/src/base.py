from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from schemas import validate_payload
from scopes import ScopePolicy

ToolHandler = Callable[[Mapping[str, Any]], Mapping[str, Any]]


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    input_schema: Mapping[str, Any]
    output_schema: Mapping[str, Any]
    scopes: list[str]


@dataclass
class Tool:
    definition: ToolDefinition
    handler: ToolHandler

    def run(self, payload: Mapping[str, Any], policy: ScopePolicy) -> Mapping[str, Any]:
        """Validate scopes and run a tool handler."""
        policy.assert_allowed(self.definition.scopes)
        validate_payload(self.definition.input_schema, payload)
        return self.handler(payload)

