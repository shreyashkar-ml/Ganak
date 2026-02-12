
from abc import ABC, abstractmethod
from typing import Iterable


class StreamClient(ABC):
    """Interface for streaming events from runner to control plane."""

    @abstractmethod
    def send(self, events: Iterable[dict]) -> None:
        raise NotImplementedError
