from dataclasses import dataclass, field


@dataclass
class PromptQueue:
    _queue: list[str] = field(default_factory=list)

    def enqueue(self, run_id: str) -> None:
        if not isinstance(run_id, str):
            raise TypeError("run_id must be str")
        self._queue.append(run_id)

    def dequeue(self) -> str | None:
        if not self._queue:
            return None
        return self._queue.pop(0)


@dataclass
class Worker:
    queue: PromptQueue

    def tick(self) -> str | None:
        """Process one queued run id."""
        if not isinstance(self.queue, PromptQueue):
            raise TypeError("queue must be PromptQueue")
        return self.queue.dequeue()
