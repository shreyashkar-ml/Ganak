
from abc import ABC, abstractmethod


class Filesystem(ABC):
    @abstractmethod
    def read_text(self, path: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def write_text(self, path: str, content: str) -> None:
        raise NotImplementedError
