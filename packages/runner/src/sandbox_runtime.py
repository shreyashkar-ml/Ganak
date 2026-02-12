from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class SandboxConfig:
    snapshot_id: str
    workdir: str


@dataclass
class Sandbox:
    config: SandboxConfig

    def start(self) -> None:
        if not isinstance(self.config, SandboxConfig):
            raise TypeError("config must be SandboxConfig")

    def stop(self) -> None:
        return None


@dataclass(frozen=True)
class ExecResult:
    exit_code: int
    stdout: str
    stderr: str


class Executor(ABC):
    @abstractmethod
    def run(self, command: str, timeout_s: int) -> ExecResult:
        raise NotImplementedError


class Filesystem(ABC):
    @abstractmethod
    def read_text(self, path: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def write_text(self, path: str, content: str) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class EgressPolicy:
    allow_internet: bool
    allowlist: list[str]


@dataclass(frozen=True)
class SecretsMount:
    mount_path: str
    handle: str
