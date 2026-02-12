from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class SessionModel:
    id: str
    repo_id: str
    status: str


@dataclass(frozen=True)
class RunModel:
    id: str
    session_id: str
    status: str


@dataclass(frozen=True)
class EventModel:
    id: str
    type: str
    session_id: str
    run_id: str
    payload: Mapping[str, object]


@dataclass(frozen=True)
class RepoModel:
    id: str
    url: str


@dataclass(frozen=True)
class ArtifactModel:
    id: str
    run_id: str
    uri: str
