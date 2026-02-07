from __future__ import annotations

from typing import Mapping, Any

from base import Tool, ToolDefinition
from scopes import ScopePolicy


def handle(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    return {"status": "sent", "channel": payload.get("channel", "")}


def build_tool() -> Tool:
    definition = ToolDefinition(
        name="slack.post",
        input_schema={"required": ["channel", "text"]},
        output_schema={"required": ["status"]},
        scopes=["notifications.send"],
    )
    return Tool(definition=definition, handler=handle)


def run_example() -> Mapping[str, Any]:
    tool = build_tool()
    policy = ScopePolicy(allowed={"notifications.send"})
    return tool.run({"channel": "alerts", "text": "hi"}, policy)

