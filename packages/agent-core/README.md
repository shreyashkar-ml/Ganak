# agent-core

Owns deterministic orchestration.

Modules:
- `agent/`
- `tools/`
- `state/`
- `protocol/`
- `patch/`
- `verification/`

Rules:
- Keep infra-independent behavior in this package.
- Emit events as primary execution trace.
