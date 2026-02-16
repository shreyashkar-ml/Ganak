from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureFlags:
    enable_verification: bool = True
    enable_auto_pr: bool = False


@dataclass(frozen=True)
class AgentSettings:
    max_steps: int = 8
    timeout_s: int = 120
