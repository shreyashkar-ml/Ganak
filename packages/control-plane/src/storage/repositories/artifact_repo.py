
from dataclasses import dataclass, field

from storage.models.artifact import ArtifactModel


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

