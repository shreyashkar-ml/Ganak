# Ganak

Hosted-first Ganak with explicit boundaries so we can add self-hosted runners later without rewrites.

## What this is
A control plane orchestrates sessions, prompts, and runs. A runner executes work inside sandboxes. Tools are pure connectors with scoped permissions. Every action emits structured events for replay and audit.

## Core concepts
- Session: user workspace with prompts and runs
- Sandbox: isolated execution environment per run
- Tool: capability with explicit input/output schema and scopes
- Event Log: append-only record of every action
- Prompt Queue: ordered inputs waiting to execute
- Repo Snapshot: reproducible image of repo state used by sandboxes

## Architecture (hosted-first)
```
User/CLI/Web
    |
    v
Control Plane  <----->  State Backend (Postgres)
    |
    v
Runner Backend (Modal now, other backends later)
    |
    v
Sandbox + Tools
```

## Option C readiness
- Transport-agnostic event protocol (JSON schemas in `contracts/`)
- Stable tool interfaces and scopes (no direct infra coupling)
- Stateless control-plane workers backed by a state backend
- Runner protocol stubs ready for self-hosted execution

## Quickstart (local)
1. Read `technical_overview.md` for prerequisites and setup.
2. Sync project environment: `uv sync`
3. Start infra: `docker compose -f infra/docker-compose.yaml up -d`
4. Run the control plane (stub server): `uv run python packages/control-plane/src/api/app.py`
5. Run the CLI: `uv run python packages/cli/src/cli.py`

Common `uv` commands:
```bash
uv sync
uv run python packages/control-plane/src/api/app.py
uv run python packages/cli/src/cli.py repo https://github.com/ganak-ai/ganak
uv run python packages/cli/src/cli.py session ganak_repo_123
uv run python packages/cli/src/cli.py run ganak_sess_123 "Fix failing test"
```

Control-plane scaling and performance knobs:
- `CONTROL_PLANE_HOST` (default `0.0.0.0`)
- `CONTROL_PLANE_PORT` (default `8000`)
- `CONTROL_PLANE_WORKERS` (default `1`)
- `CONTROL_PLANE_LIMIT_CONCURRENCY` (default `200`)
- `CONTROL_PLANE_BACKLOG` (default `2048`)
- `CONTROL_PLANE_KEEPALIVE_TIMEOUT` (default `5`)
- `CONTROL_PLANE_STATE_BACKEND` (default `memory`)

Important:
- Keep `CONTROL_PLANE_WORKERS=1` while using `CONTROL_PLANE_STATE_BACKEND=memory`.
- For multi-worker or multi-instance deployment, move to a shared durable state backend first.

## API surface
- HTTP: `POST /sessions`, `GET /sessions/{id}`, `POST /runs`, `GET /runs/{id}`, `POST /repos`
- Streaming: `/ws/stream` for session event updates

## Deployment (hosted mode)
- Reference stack: control plane service + Postgres + Modal runner backend
- Provisioning scaffolds live in `infra/terraform` and `infra/k8s/helm`
- Modal-specific assets live in `infra/modal/images` and `infra/modal/schedules`

## Security model
- Secrets are mounted into sandboxes via scoped handles
- Tool scopes enforced by policy (see `contracts/permissions/tool_scopes.yaml`)
- GitHub App auth handled in `packages/integrations/github`

## Example scenarios
- `examples/scenarios/add_feature`: deterministic feature request repo
- `examples/scenarios/fix_test_failure`: deterministic failing-test repo
- `examples/scenarios/refactor`: deterministic refactor repo

## Testing layout
- `tests/contract`: event/schema contract tests
- `tests/integration`: control-plane and runner integration tests
- `tests/e2e`: end-to-end scenario runs

## Roadmap
- Phase 0: single-session Ganak demo using CLI and Modal backend
- Phase 1A: event log streaming to multiple clients, hardened state backend, basic eval harness
- Phase 1B+: web UI and full multi-session management
