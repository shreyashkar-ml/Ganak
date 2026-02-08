

def emit_trace(name: str) -> None:
    if not isinstance(name, str):
        raise TypeError("name must be str")

