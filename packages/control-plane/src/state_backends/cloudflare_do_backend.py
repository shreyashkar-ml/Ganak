
from state_backends.interface import StateBackend


class CloudflareDoBackend(StateBackend):
    """Cloudflare Durable Objects backend placeholder."""

    def health(self) -> bool:
        return False

