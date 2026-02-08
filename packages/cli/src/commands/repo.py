
from client import ApiClient


def register_repo(client: ApiClient, url: str) -> None:
    repo = client.register_repo(url)
    print(repo)

