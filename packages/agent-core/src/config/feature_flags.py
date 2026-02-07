from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureFlags:
    enable_spawn: bool = False
    enable_streaming: bool = True

