from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GitHubAppConfig:
    app_id: str
    private_key: str

