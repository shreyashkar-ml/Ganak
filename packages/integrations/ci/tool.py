

def trigger_pipeline(pipeline: str) -> str:
    """Placeholder CI trigger."""
    if not isinstance(pipeline, str):
        raise TypeError("pipeline must be str")
    return "queued"

