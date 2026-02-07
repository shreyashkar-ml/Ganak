from __future__ import annotations

from dataclasses import dataclass, field

from storage.models.repo import RepoModel


@dataclass
class RepoRepository:
    _store: dict[str, RepoModel] = field(default_factory=dict)

    def add(self, repo: RepoModel) -> None:
        if not isinstance(repo, RepoModel):
            raise TypeError("repo must be RepoModel")
        self._store[repo.id] = repo

    def get(self, repo_id: str) -> RepoModel | None:
        if not isinstance(repo_id, str):
            raise TypeError("repo_id must be str")
        return self._store.get(repo_id)

