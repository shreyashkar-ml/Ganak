from dataclasses import dataclass


@dataclass(frozen=True)
class PullRequest:
    title: str
    body: str
    head: str
    base: str


def create_pull_request(pr: PullRequest) -> str:
    if not isinstance(pr, PullRequest):
        raise TypeError("pr must be PullRequest")
    return "https://github.com/ganak-ai/ganak/pull/1"


def send_message(channel: str, text: str) -> bool:
    if not isinstance(channel, str) or not isinstance(text, str):
        raise TypeError("channel and text must be str")
    return True


def trigger_pipeline(pipeline: str) -> str:
    if not isinstance(pipeline, str):
        raise TypeError("pipeline must be str")
    return "queued"


def send_metric(name: str, value: float) -> None:
    if not isinstance(name, str) or not isinstance(value, (int, float)):
        raise TypeError("name must be str and value must be number")


def send_error(message: str) -> None:
    if not isinstance(message, str):
        raise TypeError("message must be str")
