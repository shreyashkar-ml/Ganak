
from typing import Mapping, Any

from base import Tool, ToolDefinition
from scopes import ScopePolicy


def handle(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    return {"status": "ok", "input": dict(payload)}


def build_tool() -> Tool:
    definition = ToolDefinition(
        name="github.pr.create",
        input_schema={"required": ["repo", "title"]},
        output_schema={"required": ["url"]},
        scopes=["git.write"],
    )
    return Tool(definition=definition, handler=handle)


def run_example() -> Mapping[str, Any]:
    tool = build_tool()
    policy = ScopePolicy(allowed={"git.write"})
    return tool.run({"repo": "ganak-ai/ganak", "title": "Ganak Example"}, policy)
