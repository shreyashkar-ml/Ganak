from __future__ import annotations

import difflib
from typing import Iterable


def apply_ndiff(ndiff_lines: Iterable[str]) -> str:
    """Apply an ndiff patch and return the updated text."""
    return "\n".join(difflib.restore(list(ndiff_lines), 2))

