from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ExecResult:
    exit_code: int
    stdout: str
    stderr: str


class Executor(Protocol):
    def run(self, command: str, timeout_s: int) -> ExecResult:
        ...

