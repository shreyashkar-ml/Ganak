# API

Control-plane HTTP endpoints:
- `POST /sessions`
- `GET /sessions/{id}`
- `POST /runs`
- `GET /runs/{id}`
- `POST /repos`

Streaming endpoint:
- `GET /ws/stream` (WebSocket upgrade)

Guidance:
- Keep request/response payloads aligned to schemas in `contracts/schemas/`.
- Emit events for state transitions so clients can replay run history.
