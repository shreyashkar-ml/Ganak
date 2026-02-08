
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ScopePolicy:
    allowed: set[str]

    def assert_allowed(self, required: Iterable[str]) -> None:
        """Raise if required scopes are not allowed."""
        missing = [scope for scope in required if scope not in self.allowed]
        if missing:
            raise PermissionError(f"scopes not allowed: {', '.join(missing)}")

