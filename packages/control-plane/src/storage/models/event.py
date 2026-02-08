
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class EventModel:
    id: str
    type: str
    session_id: str
    run_id: str
    payload: Mapping[str, object]

