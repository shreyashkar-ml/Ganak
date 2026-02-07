from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from tools.tool_interface import Tool


@dataclass
class ToolRegistry:
    _tools: dict[str, Tool] = field(default_factory=dict)

    def register(self, tool: Tool) -> None:
        """Register a tool by name."""
        if not isinstance(tool, Tool):
            raise TypeError("tool must be Tool")
        name = tool.spec.name
        if name in self._tools:
            raise ValueError(f"tool already registered: {name}")
        self._tools[name] = tool

    def get(self, name: str) -> Tool:
        """Fetch a tool by name."""
        if not isinstance(name, str):
            raise TypeError("name must be str")
        if name not in self._tools:
            raise KeyError(f"unknown tool: {name}")
        return self._tools[name]

    def list(self) -> Iterable[str]:
        return list(self._tools.keys())

