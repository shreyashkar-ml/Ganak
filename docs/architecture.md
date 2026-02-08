# Architecture

Lifecycle:
1. Queue run
2. Dispatch run
3. Boot sandbox from snapshot
4. Execute tool/event loop
5. Apply patch + verification
6. Store/stream artifacts and events

Constraints:
- `agent-core` remains backend-agnostic.
- Control-plane workers are stateless.
- Tools/connectors enforce explicit scopes.
