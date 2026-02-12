def emit_trace(name: str) -> None:
    if not isinstance(name, str):
        raise TypeError("name must be str")


def log_event(message: str) -> None:
    if not isinstance(message, str):
        raise TypeError("message must be str")
