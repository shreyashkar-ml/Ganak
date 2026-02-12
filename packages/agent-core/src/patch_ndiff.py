import difflib
from typing import Iterable


def make_ndiff(original: str, updated: str) -> list[str]:
    """Return an ndiff list for two text blobs."""
    if not isinstance(original, str) or not isinstance(updated, str):
        raise TypeError("original and updated must be str")
    return list(difflib.ndiff(original.splitlines(), updated.splitlines()))


def ndiff_to_text(ndiff_lines: Iterable[str]) -> str:
    """Join ndiff lines into a patch text blob."""
    return "\n".join(list(ndiff_lines))


def apply_ndiff(ndiff_lines: Iterable[str]) -> str:
    """Apply an ndiff patch and return the updated text."""
    return "\n".join(difflib.restore(list(ndiff_lines), 2))
