
from abc import ABC, abstractmethod
from dataclasses import dataclass


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
