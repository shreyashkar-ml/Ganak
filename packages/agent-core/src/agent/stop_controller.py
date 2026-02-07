class StopController:
    """Tracks stop requests for the running agent."""

    def __init__(self) -> None:
        self._stop_requested = False

    def request_stop(self) -> None:
        self._stop_requested = True

    def should_stop(self) -> bool:
        return self._stop_requested

