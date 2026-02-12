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


def sync_repo(path: str) -> None:
    """Placeholder repo sync."""
    if not isinstance(path, str):
        raise TypeError("path must be str")


@dataclass(frozen=True)
class GitCommit:
    message: str
    author: str


def commit_changes(path: str, commit: GitCommit) -> None:
    """Placeholder commit operation."""
    if not isinstance(path, str):
        raise TypeError("path must be str")
    if not isinstance(commit, GitCommit):
        raise TypeError("commit must be GitCommit")
