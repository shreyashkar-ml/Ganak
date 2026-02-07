from __future__ import annotations

from dataclasses import dataclass

from queue.prompt_queue import PromptQueue


@dataclass
class Worker:
    queue: PromptQueue

    def tick(self) -> str | None:
        """Process one queued run id."""
        if not isinstance(self.queue, PromptQueue):
            raise TypeError("queue must be PromptQueue")
        return self.queue.dequeue()

