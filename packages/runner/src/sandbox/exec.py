
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ExecResult:
    exit_code: int
    stdout: str
    stderr: str


class Executor(ABC):
    @abstractmethod
    def run(self, command: str, timeout_s: int) -> ExecResult:
        raise NotImplementedError
