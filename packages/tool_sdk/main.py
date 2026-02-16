from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping

from shared_models import ToolContract

ToolHandler = Callable[[Mapping[str, Any]], Mapping[str, Any]]


ToolDefinition = ToolContract


@dataclass(frozen=True)
class ScopePolicy:
    allowed: set[str]

    def assert_allowed(self, required: Iterable[str]) -> None:
        missing = [scope for scope in required if scope not in self.allowed]
        if missing:
            raise PermissionError(f"scopes not allowed: {', '.join(missing)}")


@dataclass(frozen=True)
class ToolContext:
    org_id: str
    repo_id: str
    session_id: str
    run_id: str
    secrets_handle: str


def validate_payload(schema: Mapping[str, Any], payload: Mapping[str, Any]) -> None:
    if not isinstance(schema, Mapping):
        raise TypeError("schema must be a mapping")
    if not isinstance(payload, Mapping):
        raise TypeError("payload must be a mapping")
    required = schema.get("required", [])
    if required:
        if not isinstance(required, list):
            raise TypeError("schema required must be list")
        for key in required:
            if key not in payload:
                raise ValueError(f"missing required key: {key}")


def with_logging(handler: ToolHandler, name: str) -> ToolHandler:
    def wrapped(payload: Mapping[str, Any]) -> Mapping[str, Any]:
        if not isinstance(payload, Mapping):
            raise TypeError("payload must be a mapping")
        result = handler(payload)
        return {"tool": name, "result": result}

    return wrapped


@dataclass
class Tool:
    definition: ToolDefinition
    handler: ToolHandler

    def run(self, payload: Mapping[str, Any], policy: ScopePolicy) -> Mapping[str, Any]:
        policy.assert_allowed(self.definition.scopes)
        validate_payload(self.definition.input_schema, payload)
        return self.handler(payload)
