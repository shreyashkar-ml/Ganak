# Local Development

Prerequisites:
- Python 3.11+
- Docker

Baseline startup:
```bash
docker compose -f infra/docker-compose.yaml up -d
python packages/control-plane/src/api/app.py
python packages/cli/main.py
```
