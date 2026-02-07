from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CliConfig:
    api_base: str = "http://localhost:8000"

