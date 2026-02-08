from dataclasses import dataclass, field
from typing import Dict, List, Mapping

@dataclass
class ControlPlaneState:
    sessions: Dict[str, Mapping[str, str]] = field(default_factory=dict)
    runs: Dict[str, Mapping[str, str]] = field(default_factory=dict)
    events: List[Mapping[str, object]] = field(default_factory=list)
    repos: Dict[str, Mapping[str, str]] = field(default_factory=dict)