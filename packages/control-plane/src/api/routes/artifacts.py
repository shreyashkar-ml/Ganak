
from typing import Mapping

from api.state import ControlPlaneState


def list_artifacts(state: ControlPlaneState, run_id: str) -> list[Mapping[str, str]]:
    """Placeholder artifacts listing."""
    if not isinstance(state, ControlPlaneState):
        raise TypeError("state must be ControlPlaneState")
    if not isinstance(run_id, str):
        raise TypeError("run_id must be str")
    return []
