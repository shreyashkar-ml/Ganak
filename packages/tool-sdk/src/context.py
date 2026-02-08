
from dataclasses import dataclass


@dataclass(frozen=True)
class ToolContext:
    org_id: str
    repo_id: str
    session_id: str
    run_id: str
    secrets_handle: str

