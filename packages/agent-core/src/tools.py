from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Mapping

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
        if not isinstance(payload, Mapping):
            raise TypeError("payload must be a mapping")
        return self.handler(payload)


@dataclass
class ToolRegistry:
    _tools: dict[str, Tool] = field(default_factory=dict)

    def register(self, tool: Tool) -> None:
        if not isinstance(tool, Tool):
            raise TypeError("tool must be Tool")
        name = tool.spec.name
        if name in self._tools:
            raise ValueError(f"tool already registered: {name}")
        self._tools[name] = tool

    def get(self, name: str) -> Tool:
        if not isinstance(name, str):
            raise TypeError("name must be str")
        if name not in self._tools:
            raise KeyError(f"unknown tool: {name}")
        return self._tools[name]

    def list(self) -> Iterable[str]:
        return list(self._tools.keys())


@dataclass(frozen=True)
class ShellResult:
    exit_code: int
    stdout: str
    stderr: str


class SandboxProxy(ABC):
    """Backend interface for executing operations inside a sandbox."""

    @abstractmethod
    def run(self, command: str, timeout_s: int) -> ShellResult:
        raise NotImplementedError

    @abstractmethod
    def read_file(self, path: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def write_file(self, path: str, content: str) -> None:
        raise NotImplementedError
