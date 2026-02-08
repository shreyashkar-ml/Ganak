# Hosted Deployment

Baseline stack:
- Control plane
- Postgres
- Runner backend (Modal)

Notes:
- Infra scaffolding lives under `infra/`.
- Secrets should be cloud-managed and scoped per environment.
