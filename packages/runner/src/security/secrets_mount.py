
from dataclasses import dataclass


@dataclass(frozen=True)
class SecretsMount:
    mount_path: str
    handle: str

