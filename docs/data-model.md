# Data Model

Entity graph:
`Org -> Users/Repos -> Sessions -> Runs -> Steps`

Run outputs:
- `Events`
- `Artifacts`
- `ToolCall` records

Guidance:
- Persist events as append-only log entries.
- Keep IDs stable and traceable across session/run boundaries.
