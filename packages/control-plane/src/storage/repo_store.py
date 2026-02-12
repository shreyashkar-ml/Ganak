from dataclasses import dataclass, field

from storage.records import ArtifactModel, EventModel, RepoModel, RunModel, SessionModel


@dataclass
class SessionRepository:
    _store: dict[str, SessionModel] = field(default_factory=dict)

    def add(self, session: SessionModel) -> None:
        if not isinstance(session, SessionModel):
            raise TypeError("session must be SessionModel")
        self._store[session.id] = session

    def get(self, session_id: str) -> SessionModel | None:
        if not isinstance(session_id, str):
            raise TypeError("session_id must be str")
        return self._store.get(session_id)


@dataclass
class RunRepository:
    _store: dict[str, RunModel] = field(default_factory=dict)

    def add(self, run: RunModel) -> None:
        if not isinstance(run, RunModel):
            raise TypeError("run must be RunModel")
        self._store[run.id] = run

    def get(self, run_id: str) -> RunModel | None:
        if not isinstance(run_id, str):
            raise TypeError("run_id must be str")
        return self._store.get(run_id)


@dataclass
class EventRepository:
    _store: list[EventModel] = field(default_factory=list)

    def add(self, event: EventModel) -> None:
        if not isinstance(event, EventModel):
            raise TypeError("event must be EventModel")
        self._store.append(event)

    def list_for_session(self, session_id: str) -> list[EventModel]:
        if not isinstance(session_id, str):
            raise TypeError("session_id must be str")
        return [event for event in self._store if event.session_id == session_id]


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


@dataclass
class ArtifactRepository:
    _store: dict[str, ArtifactModel] = field(default_factory=dict)

    def add(self, artifact: ArtifactModel) -> None:
        if not isinstance(artifact, ArtifactModel):
            raise TypeError("artifact must be ArtifactModel")
        self._store[artifact.id] = artifact

    def get(self, artifact_id: str) -> ArtifactModel | None:
        if not isinstance(artifact_id, str):
            raise TypeError("artifact_id must be str")
        return self._store.get(artifact_id)
