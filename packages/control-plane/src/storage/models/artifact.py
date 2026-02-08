
from dataclasses import dataclass


@dataclass(frozen=True)
class ArtifactModel:
    id: str
    run_id: str
    uri: str

