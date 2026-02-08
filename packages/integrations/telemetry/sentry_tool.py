

def send_error(message: str) -> None:
    if not isinstance(message, str):
        raise TypeError("message must be str")

