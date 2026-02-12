from dataclasses import dataclass


@dataclass(frozen=True)
class GitHubAppConfig:
    app_id: str
    private_key: str


@dataclass(frozen=True)
class Token:
    value: str
    scopes: list[str]


@dataclass(frozen=True)
class Org:
    id: str
    name: str
