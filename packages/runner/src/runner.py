from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable


@dataclass(frozen=True)
class RunnerJob:
    job_id: str
    session_id: str
    run_id: str
    snapshot_id: str


class RunnerBackend(ABC):
    """Backend interface for executing runner jobs."""

    @abstractmethod
    def submit_job(self, job: RunnerJob) -> None:
        raise NotImplementedError

    @abstractmethod
    def cancel_job(self, job_id: str) -> None:
        raise NotImplementedError


class ModalBackend(RunnerBackend):
    def submit_job(self, job: RunnerJob) -> None:
        if not isinstance(job, RunnerJob):
            raise TypeError("job must be RunnerJob")
        raise NotImplementedError("Modal backend submission not wired")

    def cancel_job(self, job_id: str) -> None:
        if not isinstance(job_id, str):
            raise TypeError("job_id must be str")
        raise NotImplementedError("Modal backend cancellation not wired")


class DockerBackend(RunnerBackend):
    def submit_job(self, job: RunnerJob) -> None:
        if not isinstance(job, RunnerJob):
            raise TypeError("job must be RunnerJob")
        raise NotImplementedError("Docker backend not implemented")

    def cancel_job(self, job_id: str) -> None:
        if not isinstance(job_id, str):
            raise TypeError("job_id must be str")
        raise NotImplementedError("Docker backend not implemented")


class K8sBackend(RunnerBackend):
    def submit_job(self, job: RunnerJob) -> None:
        if not isinstance(job, RunnerJob):
            raise TypeError("job must be RunnerJob")
        raise NotImplementedError("K8s backend not implemented")

    def cancel_job(self, job_id: str) -> None:
        if not isinstance(job_id, str):
            raise TypeError("job_id must be str")
        raise NotImplementedError("K8s backend not implemented")


@dataclass(frozen=True)
class SnapshotRequest:
    repo_id: str
    commit: str


@dataclass(frozen=True)
class SnapshotResult:
    snapshot_id: str


def build_snapshot(request: SnapshotRequest) -> SnapshotResult:
    if not isinstance(request, SnapshotRequest):
        raise TypeError("request must be SnapshotRequest")
    snapshot_id = f"{request.repo_id}-{request.commit}"
    return SnapshotResult(snapshot_id=snapshot_id)


@dataclass
class SnapshotCache:
    _cache: dict[str, str] = field(default_factory=dict)

    def get(self, key: str) -> str | None:
        if not isinstance(key, str):
            raise TypeError("key must be str")
        return self._cache.get(key)

    def set(self, key: str, snapshot_id: str) -> None:
        if not isinstance(key, str) or not isinstance(snapshot_id, str):
            raise TypeError("key and snapshot_id must be str")
        self._cache[key] = snapshot_id


def snapshot_name(repo_id: str, commit: str) -> str:
    if not isinstance(repo_id, str) or not isinstance(commit, str):
        raise TypeError("repo_id and commit must be str")
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{repo_id}-{commit}-{ts}"


@dataclass(frozen=True)
class CheckoutRequest:
    repo_url: str
    commit: str


def checkout_repo(request: CheckoutRequest) -> str:
    if not isinstance(request, CheckoutRequest):
        raise TypeError("request must be CheckoutRequest")
    return f"/tmp/{request.repo_url.replace('/', '_')}/{request.commit}"


def sync_repo(path: str) -> None:
    if not isinstance(path, str):
        raise TypeError("path must be str")


@dataclass(frozen=True)
class GitCommit:
    message: str
    author: str


def commit_changes(path: str, commit: GitCommit) -> None:
    if not isinstance(path, str):
        raise TypeError("path must be str")
    if not isinstance(commit, GitCommit):
        raise TypeError("commit must be GitCommit")


class StreamClient(ABC):
    """Interface for streaming events from runner to control plane."""

    @abstractmethod
    def send(self, events: Iterable[dict]) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class SandboxConfig:
    snapshot_id: str
    workdir: str


@dataclass
class Sandbox:
    config: SandboxConfig

    def start(self) -> None:
        if not isinstance(self.config, SandboxConfig):
            raise TypeError("config must be SandboxConfig")

    def stop(self) -> None:
        return None


@dataclass(frozen=True)
class ExecResult:
    exit_code: int
    stdout: str
    stderr: str


class Executor(ABC):
    @abstractmethod
    def run(self, command: str, timeout_s: int) -> ExecResult:
        raise NotImplementedError


class Filesystem(ABC):
    @abstractmethod
    def read_text(self, path: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def write_text(self, path: str, content: str) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class EgressPolicy:
    allow_internet: bool
    allowlist: list[str]


@dataclass(frozen=True)
class SecretsMount:
    mount_path: str
    handle: str
