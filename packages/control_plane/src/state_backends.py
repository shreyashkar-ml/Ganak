from abc import ABC, abstractmethod


class StateBackend(ABC):
    """Durable backend for session/run/event state."""

    @abstractmethod
    def health(self) -> bool:
        raise NotImplementedError


class PostgresBackend(StateBackend):
    """Postgres backend placeholder."""

    def health(self) -> bool:
        return False


class CloudflareDoBackend(StateBackend):
    """Cloudflare Durable Objects backend placeholder."""

    def health(self) -> bool:
        return False
