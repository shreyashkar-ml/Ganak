from dataclasses import dataclass
from typing import Iterable, Mapping

from agent.planner import PlanStep, plan_from_prompt
from agent.policies import RunPolicy
from agent.stop_controller import StopController
from protocol.events import (
    event_run_finished,
    event_run_started,
    event_step_finished,
    event_step_started,
)
from state.event_log import EventLog
from tools.tool_registry import ToolRegistry


@dataclass(frozen=True)
class AgentInput:
    session_id: str
    run_id: str
    prompt: str


@dataclass(frozen=True)
class AgentResult:
    steps_executed: int
    stopped: bool


def run_agent_loop(
    agent_input: AgentInput,
    tool_registry: ToolRegistry,
    event_log: EventLog,
    policy: RunPolicy,
    stop_controller: StopController,
) -> AgentResult:
    """Run a deterministic agent loop over planned steps."""
    if not isinstance(agent_input, AgentInput):
        raise TypeError("agent_input must be AgentInput")
    if not isinstance(tool_registry, ToolRegistry):
        raise TypeError("tool_registry must be ToolRegistry")
    if not isinstance(event_log, EventLog):
        raise TypeError("event_log must be EventLog")
    if not isinstance(policy, RunPolicy):
        raise TypeError("policy must be RunPolicy")
    if not isinstance(stop_controller, StopController):
        raise TypeError("stop_controller must be StopController")

    event_log.append(event_run_started(agent_input.session_id, agent_input.run_id, agent_input.prompt))
    steps = plan_from_prompt(agent_input.prompt)
    steps_executed = 0

    for step in _limit_steps(steps, policy.max_steps):
        if stop_controller.should_stop():
            break
        event_log.append(event_step_started(agent_input.session_id, agent_input.run_id, step.description))
        _execute_step(step, tool_registry)
        event_log.append(event_step_finished(agent_input.session_id, agent_input.run_id, step.description))
        steps_executed += 1

    event_log.append(event_run_finished(agent_input.session_id, agent_input.run_id, stop_controller.should_stop()))
    return AgentResult(steps_executed=steps_executed, stopped=stop_controller.should_stop())


def _limit_steps(steps: Iterable[PlanStep], max_steps: int) -> Iterable[PlanStep]:
    """Yield at most max_steps items from a plan."""
    if not isinstance(max_steps, int):
        raise TypeError("max_steps must be int")
    count = 0
    for step in steps:
        if count >= max_steps:
            return
        count += 1
        yield step


def _execute_step(step: PlanStep, tool_registry: ToolRegistry) -> None:
    """Execute a single step by calling a tool if specified."""
    if not isinstance(step, PlanStep):
        raise TypeError("step must be PlanStep")
    if step.tool_name is None:
        return
    tool = tool_registry.get(step.tool_name)
    tool.run(step.tool_input or {})

