
from client import ApiClient


def create_run(client: ApiClient, session_id: str, prompt: str) -> None:
    run = client.create_run(session_id, prompt)
    print(run)

