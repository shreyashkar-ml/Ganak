
from dataclasses import dataclass


@dataclass(frozen=True)
class CheckoutRequest:
    repo_url: str
    commit: str


def checkout_repo(request: CheckoutRequest) -> str:
    """Placeholder checkout that returns a path string."""
    if not isinstance(request, CheckoutRequest):
        raise TypeError("request must be CheckoutRequest")
    return f"/tmp/{request.repo_url.replace('/', '_')}/{request.commit}"

