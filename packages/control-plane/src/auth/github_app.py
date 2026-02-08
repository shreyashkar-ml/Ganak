
from dataclasses import dataclass


@dataclass(frozen=True)
class GitHubAppConfig:
    app_id: str
    private_key: str

