"""Human-readable binary byte counts (B, KiB, MiB, GiB, TiB)."""

import re

_UNITS = {
    "b": 1,
    "kib": 1024,
    "mib": 1024 ** 2,
    "gib": 1024 ** 3,
    "tib": 1024 ** 4,
}

_ORDER = [
    ("TiB", "tib"),
    ("GiB", "gib"),
    ("MiB", "mib"),
    ("KiB", "kib"),
    ("B", "b"),
]

_PATTERN = re.compile(r"^\s*(?P<num>\d+(?:\.\d+)?|\.\d+)\s*(?P<unit>[A-Za-z]+)\s*$")


def format_bytes(count: int) -> str:
    """Format a non-negative integer byte count as a binary string.

    Counts below one KiB stay whole ('512 B'); larger counts use one
    decimal place ('1.5 KiB', '2.0 MiB'). Raises ValueError when count is
    negative or not an integer.
    """
    if not isinstance(count, int) or count < 0:
        raise ValueError(f"count must be a non-negative integer, got {count!r}")

    for label, key in _ORDER:
        factor = _UNITS[key]
        if count >= factor:
            if factor == 1:
                return f"{count} B"
            return f"{count / factor:.1f} {label}"

    return f"{count} B"


def parse_bytes(text: str) -> int:
    """Parse a binary byte-count string back into whole bytes.

    Accepts the same unit spellings case-insensitively, with or without a
    separating space ('512 B', '512b', '2.0 MiB', '1.5kib'). Raises
    ValueError for negatives, unknown units, and malformed numbers.
    """
    if not isinstance(text, str):
        raise ValueError(f"byte count must be a string, got {text!r}")

    match = _PATTERN.match(text)
    if not match:
        raise ValueError(f"malformed byte count: {text!r}")

    unit = match.group("unit").lower()
    if unit not in _UNITS:
        raise ValueError(f"unknown unit {match.group('unit')!r} in {text!r}")

    factor = _UNITS[unit]
    return round(float(match.group("num")) * factor)
