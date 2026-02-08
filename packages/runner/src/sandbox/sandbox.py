
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

