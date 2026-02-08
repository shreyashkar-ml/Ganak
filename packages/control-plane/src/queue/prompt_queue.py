from dataclasses import dataclass, field
from typing import List


@dataclass
class PromptQueue:
    _queue: List[str] = field(default_factory=list)

    def enqueue(self, run_id: str) -> None:
        if not isinstance(run_id, str):
            raise TypeError("run_id must be str")
        self._queue.append(run_id)

    def dequeue(self) -> str | None:
        if not self._queue:
            return None
        return self._queue.pop(0)

