from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ShellResult:
    exit_code: int
    stdout: str
    stderr: str


class SandboxProxy(Protocol):
    """Backend interface for executing operations inside a sandbox."""

    def run(self, command: str, timeout_s: int) -> ShellResult:
        ...

    def read_file(self, path: str) -> str:
        ...

    def write_file(self, path: str, content: str) -> None:
        ...

