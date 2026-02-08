"""Minimal end-to-end skeleton of the Ganak agentic system.

This file compresses the core architecture into one script so the interactions
between control-plane, runner, agent-core, tool layer, and integrations are easy
to inspect and debug.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Mapping
import uuid


def utc_now_iso() -> str:
    """Return a UTC ISO timestamp."""
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    """Generate a stable prefixed identifier."""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


@dataclass(frozen=True)
class EventEnvelope:
    """Event contract shared across components."""

    id: str
    ts: str
    type: str
    session_id: str
    run_id: str
    payload: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Serialize envelope to plain dictionary."""
        return {
            "id": self.id,
            "ts": self.ts,
            "type": self.type,
            "session_id": self.session_id,
            "run_id": self.run_id,
            "payload": dict(self.payload),
        }


def make_event(event_type: str, session_id: str, run_id: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    """Construct a typed event envelope."""
    return EventEnvelope(
        id=new_id("evt"),
        ts=utc_now_iso(),
        type=event_type,
        session_id=session_id,
        run_id=run_id,
        payload=payload,
    ).to_dict()


@dataclass
class EventLog:
    """Append-only event storage."""

    events: list[dict[str, Any]] = field(default_factory=list)

    def append(self, event: Mapping[str, Any]) -> None:
        """Append one event."""
        if not isinstance(event, Mapping):
            raise TypeError("event must be Mapping")
        self.events.append(dict(event))

    def list_for_session(self, session_id: str) -> list[dict[str, Any]]:
        """List events for one session."""
        if not isinstance(session_id, str):
            raise TypeError("session_id must be str")
        return [event for event in self.events if event.get("session_id") == session_id]


@dataclass(frozen=True)
class SessionRecord:
    """Session model."""

    id: str
    repo_id: str
    status: str


@dataclass(frozen=True)
class RunRecord:
    """Run model."""

    id: str
    session_id: str
    prompt: str
    status: str


@dataclass
class PromptQueue:
    """FIFO queue of run IDs."""

    items: list[str] = field(default_factory=list)

    def enqueue(self, run_id: str) -> None:
        """Enqueue one run ID."""
        if not isinstance(run_id, str):
            raise TypeError("run_id must be str")
        self.items.append(run_id)

    def dequeue(self) -> str | None:
        """Pop one run ID from queue."""
        if not self.items:
            return None
        return self.items.pop(0)


@dataclass
class ConcurrencyLimits:
    """Dispatch limit configuration."""

    max_active_runs: int
    active_runs: int = 0

    def can_dispatch(self) -> bool:
        """Return whether a run can be dispatched now."""
        return self.active_runs < self.max_active_runs

    def mark_dispatched(self) -> None:
        """Increase active run count."""
        self.active_runs += 1

    def mark_finished(self) -> None:
        """Decrease active run count."""
        self.active_runs = max(0, self.active_runs - 1)


@dataclass(frozen=True)
class PlanStep:
    """Single step in an agent plan."""

    description: str
    tool_name: str | None = None
    tool_input: dict[str, Any] | None = None


def plan_from_prompt(prompt: str) -> list[PlanStep]:
    """Create a minimal deterministic plan from prompt text."""
    if not isinstance(prompt, str):
        raise TypeError("prompt must be str")
    text = prompt.strip()
    if not text:
        return []
    steps: list[PlanStep] = [PlanStep(description=f"Analyze prompt: {text}")]
    steps.append(PlanStep(description="Read README", tool_name="repo.read", tool_input={"path": "README.md"}))
    if "pr" in text.lower() or "pull request" in text.lower():
        steps.append(
            PlanStep(
                description="Open pull request",
                tool_name="github.pr.create",
                tool_input={
                    "repo": "ganak-ai/ganak",
                    "title": "Automated Ganak patch",
                    "head": "agent/minimal",
                    "base": "main",
                },
            )
        )
    return steps


ToolHandler = Callable[[Mapping[str, Any]], Mapping[str, Any]]


@dataclass(frozen=True)
class ToolDefinition:
    """Tool contract with required fields and scopes."""

    name: str
    required_input_keys: list[str]
    scopes: list[str]


@dataclass(frozen=True)
class ScopePolicy:
    """Allowed scope set."""

    allowed: set[str]

    def assert_allowed(self, required: Iterable[str]) -> None:
        """Enforce required scopes."""
        missing = [scope for scope in required if scope not in self.allowed]
        if missing:
            raise PermissionError(f"missing scopes: {', '.join(missing)}")


@dataclass
class Tool:
    """Runtime tool wrapper."""

    definition: ToolDefinition
    handler: ToolHandler

    def run(self, payload: Mapping[str, Any], policy: ScopePolicy) -> Mapping[str, Any]:
        """Validate payload and execute tool handler."""
        if not isinstance(payload, Mapping):
            raise TypeError("payload must be Mapping")
        policy.assert_allowed(self.definition.scopes)
        for key in self.definition.required_input_keys:
            if key not in payload:
                raise ValueError(f"missing required input key: {key}")
        return self.handler(payload)


@dataclass
class ToolRegistry:
    """Map tool name to tool implementation."""

    tools: dict[str, Tool] = field(default_factory=dict)

    def register(self, tool: Tool) -> None:
        """Register one tool."""
        if not isinstance(tool, Tool):
            raise TypeError("tool must be Tool")
        name = tool.definition.name
        if name in self.tools:
            raise ValueError(f"duplicate tool: {name}")
        self.tools[name] = tool

    def get(self, name: str) -> Tool:
        """Get one tool by name."""
        if name not in self.tools:
            raise KeyError(f"unknown tool: {name}")
        return self.tools[name]


class StopController:
    """In-process stop flag."""

    def __init__(self) -> None:
        self._stop = False

    def request_stop(self) -> None:
        """Request run stop."""
        self._stop = True

    def should_stop(self) -> bool:
        """Return whether stop was requested."""
        return self._stop


@dataclass(frozen=True)
class RunPolicy:
    """Run limits."""

    max_steps: int = 8


@dataclass(frozen=True)
class AgentInput:
    """Agent loop input."""

    session_id: str
    run_id: str
    prompt: str


@dataclass(frozen=True)
class AgentResult:
    """Agent loop result."""

    steps_executed: int
    stopped: bool


def run_agent_loop(
    agent_input: AgentInput,
    tool_registry: ToolRegistry,
    scope_policy: ScopePolicy,
    event_log: EventLog,
    policy: RunPolicy,
    stop_controller: StopController,
) -> AgentResult:
    """Execute planned steps, invoke tools, and emit events."""
    event_log.append(make_event("run_started", agent_input.session_id, agent_input.run_id, {"prompt": agent_input.prompt}))
    steps_executed = 0
    for step in plan_from_prompt(agent_input.prompt):
        if steps_executed >= policy.max_steps:
            break
        if stop_controller.should_stop():
            break
        event_log.append(make_event("step_started", agent_input.session_id, agent_input.run_id, {"description": step.description}))
        if step.tool_name is not None:
            tool = tool_registry.get(step.tool_name)
            output = tool.run(step.tool_input or {}, scope_policy)
            event_log.append(
                make_event(
                    "tool_result",
                    agent_input.session_id,
                    agent_input.run_id,
                    {"name": step.tool_name, "output": output, "success": True},
                )
            )
        event_log.append(make_event("step_finished", agent_input.session_id, agent_input.run_id, {"description": step.description}))
        steps_executed += 1
    event_log.append(make_event("run_finished", agent_input.session_id, agent_input.run_id, {"stopped": stop_controller.should_stop()}))
    return AgentResult(steps_executed=steps_executed, stopped=stop_controller.should_stop())


@dataclass(frozen=True)
class SnapshotRequest:
    """Snapshot build input."""

    repo_id: str
    commit: str


@dataclass(frozen=True)
class SnapshotResult:
    """Snapshot build output."""

    snapshot_id: str


def build_snapshot(request: SnapshotRequest) -> SnapshotResult:
    """Build a deterministic snapshot ID."""
    if not isinstance(request, SnapshotRequest):
        raise TypeError("request must be SnapshotRequest")
    return SnapshotResult(snapshot_id=f"{request.repo_id}-{request.commit}")


@dataclass(frozen=True)
class RunnerJob:
    """Runner job contract."""

    job_id: str
    session_id: str
    run_id: str
    snapshot_id: str


class RunnerBackend(ABC):
    """Mandatory runner backend interface."""

    @abstractmethod
    def submit_job(self, job: RunnerJob) -> None:
        """Submit a runner job."""
        raise NotImplementedError

    @abstractmethod
    def cancel_job(self, job_id: str) -> None:
        """Cancel a runner job."""
        raise NotImplementedError


@dataclass
class LocalRunnerBackend(RunnerBackend):
    """In-memory runner backend for local skeleton execution."""

    state: "ControlPlaneState"
    tool_registry: ToolRegistry
    scope_policy: ScopePolicy

    def submit_job(self, job: RunnerJob) -> None:
        """Run the agent loop immediately for the submitted job."""
        run = self.state.runs[job.run_id]
        agent_input = AgentInput(session_id=job.session_id, run_id=job.run_id, prompt=run.prompt)
        result = run_agent_loop(
            agent_input=agent_input,
            tool_registry=self.tool_registry,
            scope_policy=self.scope_policy,
            event_log=self.state.event_log,
            policy=RunPolicy(max_steps=6),
            stop_controller=StopController(),
        )
        self.state.runs[job.run_id] = RunRecord(
            id=run.id,
            session_id=run.session_id,
            prompt=run.prompt,
            status="finished" if not result.stopped else "stopped",
        )
        self.state.limits.mark_finished()

    def cancel_job(self, job_id: str) -> None:
        """Cancel is a no-op in this minimal backend."""
        if not isinstance(job_id, str):
            raise TypeError("job_id must be str")
        return None


@dataclass
class ControlPlaneState:
    """Control-plane state container."""

    sessions: dict[str, SessionRecord] = field(default_factory=dict)
    runs: dict[str, RunRecord] = field(default_factory=dict)
    event_log: EventLog = field(default_factory=EventLog)
    queue: PromptQueue = field(default_factory=PromptQueue)
    limits: ConcurrencyLimits = field(default_factory=lambda: ConcurrencyLimits(max_active_runs=2))


@dataclass
class ControlPlane:
    """Minimal control-plane with session/run lifecycle and dispatch."""

    state: ControlPlaneState
    runner: RunnerBackend

    def create_session(self, repo_id: str) -> SessionRecord:
        """Create one active session."""
        if not isinstance(repo_id, str):
            raise TypeError("repo_id must be str")
        session = SessionRecord(id=new_id("sess"), repo_id=repo_id, status="active")
        self.state.sessions[session.id] = session
        return session

    def create_run(self, session_id: str, prompt: str) -> RunRecord:
        """Create one queued run and emit initial event."""
        if session_id not in self.state.sessions:
            raise KeyError(f"unknown session: {session_id}")
        run = RunRecord(id=new_id("run"), session_id=session_id, prompt=prompt, status="queued")
        self.state.runs[run.id] = run
        self.state.event_log.append(make_event("run_queued", session_id, run.id, {"prompt": prompt}))
        self.state.queue.enqueue(run.id)
        return run

    def process_once(self) -> bool:
        """Dispatch one queued run if capacity allows."""
        run_id = self.state.queue.dequeue()
        if run_id is None:
            return False
        if not self.state.limits.can_dispatch():
            self.state.queue.enqueue(run_id)
            self.state.event_log.append(
                make_event(
                    "run_dispatch_blocked",
                    self.state.runs[run_id].session_id,
                    run_id,
                    {"active_runs": self.state.limits.active_runs, "max_active_runs": self.state.limits.max_active_runs},
                )
            )
            return False
        run = self.state.runs[run_id]
        self.state.runs[run_id] = RunRecord(id=run.id, session_id=run.session_id, prompt=run.prompt, status="dispatched")
        self.state.limits.mark_dispatched()
        self.state.event_log.append(make_event("run_dispatched", run.session_id, run_id, {}))
        snapshot = build_snapshot(SnapshotRequest(repo_id=self.state.sessions[run.session_id].repo_id, commit="HEAD"))
        job = RunnerJob(job_id=new_id("job"), session_id=run.session_id, run_id=run_id, snapshot_id=snapshot.snapshot_id)
        self.runner.submit_job(job)
        return True

    def stream_events(self, session_id: str) -> list[dict[str, Any]]:
        """Return all events for one session."""
        return self.state.event_log.list_for_session(session_id)


def make_default_registry() -> ToolRegistry:
    """Create a minimal tool registry for the demo."""
    registry = ToolRegistry()
    registry.register(
        Tool(
            definition=ToolDefinition(name="repo.read", required_input_keys=["path"], scopes=["repo.read"]),
            handler=lambda payload: {"path": payload["path"], "content": "# Ganak\n"},
        )
    )
    registry.register(
        Tool(
            definition=ToolDefinition(
                name="github.pr.create",
                required_input_keys=["repo", "title", "head", "base"],
                scopes=["git.write"],
            ),
            handler=lambda payload: {
                "url": f"https://github.com/{payload['repo']}/pull/1",
                "title": payload["title"],
            },
        )
    )
    return registry


def demo() -> None:
    """Run a minimal end-to-end flow and print event stream."""
    state = ControlPlaneState()
    registry = make_default_registry()
    policy = ScopePolicy(allowed={"repo.read", "git.write"})
    runner = LocalRunnerBackend(state=state, tool_registry=registry, scope_policy=policy)
    control_plane = ControlPlane(state=state, runner=runner)

    session = control_plane.create_session(repo_id="ganak_repo_demo")
    run = control_plane.create_run(session_id=session.id, prompt="Fix failing test and open PR")
    control_plane.process_once()

    print(f"session={session.id} run={run.id}")
    for event in control_plane.stream_events(session.id):
        print(f"{event['type']}: {event['payload']}")


if __name__ == "__main__":
    demo()
