
from dataclasses import dataclass


@dataclass(frozen=True)
class SessionModel:
    id: str
    repo_id: str
    status: str

