
from typing import Mapping, Any

from tool_sdk import Tool, ToolDefinition
from tool_sdk import ScopePolicy


def handle(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    return {"status": "queued", "pipeline": payload.get("pipeline", "")}


def build_tool() -> Tool:
    definition = ToolDefinition(
        name="ci.run",
        input_schema={"required": ["pipeline"]},
        output_schema={"required": ["status"]},
        scopes=["ci.run"],
    )
    return Tool(definition=definition, handler=handle)


def run_example() -> Mapping[str, Any]:
    tool = build_tool()
    policy = ScopePolicy(allowed={"ci.run"})
    return tool.run({"pipeline": "test"}, policy)

