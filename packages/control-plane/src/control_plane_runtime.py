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


def emit_trace(name: str) -> None:
    if not isinstance(name, str):
        raise TypeError("name must be str")


def log_event(message: str) -> None:
    if not isinstance(message, str):
        raise TypeError("message must be str")
