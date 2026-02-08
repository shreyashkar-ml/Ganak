
from abc import ABC, abstractmethod


class StateBackend(ABC):
    """Durable backend for session/run/event state."""

    @abstractmethod
    def health(self) -> bool:
        raise NotImplementedError
