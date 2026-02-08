
from state_backends.interface import StateBackend


class PostgresBackend(StateBackend):
    """Postgres backend placeholder."""

    def health(self) -> bool:
        return False

