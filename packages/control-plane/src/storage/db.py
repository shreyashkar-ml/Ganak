
from dataclasses import dataclass


@dataclass(frozen=True)
class DbConfig:
    dsn: str

