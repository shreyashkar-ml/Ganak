from __future__ import annotations

from typing import Any, Mapping


def validate_payload(schema: Mapping[str, Any], payload: Mapping[str, Any]) -> None:
    """Validate payload against a minimal schema with required keys."""
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

