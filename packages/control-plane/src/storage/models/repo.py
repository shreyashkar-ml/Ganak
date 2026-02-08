
from dataclasses import dataclass


@dataclass(frozen=True)
class RepoModel:
    id: str
    url: str

