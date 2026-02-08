"""Minimal agent-core and tool-sdk skeleton."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Mapping
import uuid


def utc_now_iso() -> str:
    """Return UTC timestamp string."""
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    """Return prefixed ID."""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


@dataclass(frozen=True)
class EventEnvelope:
    """Event schema envelope."""

    id: str
    ts: str
    type: str
    session_id: str
    run_id: str
    payload: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
        return {
            "id": self.id,
            "ts": self.ts,
            "type": self.type,
            "session_id": self.session_id,
            "run_id": self.run_id,
            "payload": dict(self.payload),
        }


def make_event(event_type: str, session_id: str, run_id: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    """Create one event envelope."""
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
    """Append-only event log."""

    events: list[dict[str, Any]] = field(default_factory=list)

    def append(self, event: Mapping[str, Any]) -> None:
        """Append one event."""
        if not isinstance(event, Mapping):
            raise TypeError("event must be Mapping")
        self.events.append(dict(event))

    def list_for_session(self, session_id: str) -> list[dict[str, Any]]:
        """List events by session."""
        if not isinstance(session_id, str):
            raise TypeError("session_id must be str")
        return [event for event in self.events if event.get("session_id") == session_id]


@dataclass(frozen=True)
class PlanStep:
    """Plan step object."""

    description: str
    tool_name: str | None = None
    tool_input: dict[str, Any] | None = None


def plan_from_prompt(prompt: str) -> list[PlanStep]:
    """Generate a tiny deterministic plan."""
    if not isinstance(prompt, str):
        raise TypeError("prompt must be str")
    text = prompt.strip()
    if not text:
        return []
    steps = [PlanStep(description=f"Analyze prompt: {text}")]
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
    """Tool contract."""

    name: str
    required_input_keys: list[str]
    scopes: list[str]


@dataclass(frozen=True)
class ScopePolicy:
    """Allowed scope set."""

    allowed: set[str]

    def assert_allowed(self, required: Iterable[str]) -> None:
        """Ensure required scopes are allowed."""
        missing = [scope for scope in required if scope not in self.allowed]
        if missing:
            raise PermissionError(f"missing scopes: {', '.join(missing)}")


@dataclass
class Tool:
    """Tool runtime wrapper."""

    definition: ToolDefinition
    handler: ToolHandler

    def run(self, payload: Mapping[str, Any], policy: ScopePolicy) -> Mapping[str, Any]:
        """Validate and execute tool."""
        if not isinstance(payload, Mapping):
            raise TypeError("payload must be Mapping")
        policy.assert_allowed(self.definition.scopes)
        for key in self.definition.required_input_keys:
            if key not in payload:
                raise ValueError(f"missing required input key: {key}")
        return self.handler(payload)


@dataclass
class ToolRegistry:
    """Tool lookup registry."""

    tools: dict[str, Tool] = field(default_factory=dict)

    def register(self, tool: Tool) -> None:
        """Register tool by definition name."""
        if not isinstance(tool, Tool):
            raise TypeError("tool must be Tool")
        name = tool.definition.name
        if name in self.tools:
            raise ValueError(f"duplicate tool: {name}")
        self.tools[name] = tool

    def get(self, name: str) -> Tool:
        """Get registered tool."""
        if name not in self.tools:
            raise KeyError(f"unknown tool: {name}")
        return self.tools[name]


class StopController:
    """Stop signal container."""

    def __init__(self) -> None:
        self._stop = False

    def request_stop(self) -> None:
        """Request stopping run loop."""
        self._stop = True

    def should_stop(self) -> bool:
        """Return stop status."""
        return self._stop


@dataclass(frozen=True)
class RunPolicy:
    """Run execution policy."""

    max_steps: int = 8


@dataclass(frozen=True)
class AgentInput:
    """Agent loop input."""

    session_id: str
    run_id: str
    prompt: str


@dataclass(frozen=True)
class AgentResult:
    """Agent loop output."""

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
    """Execute plan steps and emit lifecycle events."""
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


def make_default_registry() -> ToolRegistry:
    """Create tiny default tool set."""
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
