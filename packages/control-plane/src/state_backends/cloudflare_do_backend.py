from __future__ import annotations

from state_backends.interface import StateBackend


class CloudflareDoBackend(StateBackend):
    """Cloudflare Durable Objects backend placeholder."""

    def health(self) -> bool:
        return False

