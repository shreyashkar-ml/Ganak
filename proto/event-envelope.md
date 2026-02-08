# Event Envelope

All cross-boundary events use a stable envelope with:
- `id`
- `ts`
- `type`
- `session_id`
- `run_id`
- `payload`

Guidance:
- Preserve envelope stability across control-plane and runner boundaries.
