"""Compact duration strings using units d, h, m, s."""

_UNITS = {
    "d": 86400,
    "h": 3600,
    "m": 60,
    "s": 1,
}

_ORDER = list(_UNITS)


def parse_duration(text: str) -> int:
    """Parse a compact duration string into whole seconds.

    ``text`` is one or more value-unit pairs with strictly descending units
    (d > h > m > s), each appearing at most once. An optional single leading
    ``-`` negates the whole duration.
    """
    if not isinstance(text, str):
        raise ValueError(f"duration must be a string, got {text!r}")

    negative = False
    if text.startswith("-"):
        negative = True
        text = text[1:]

    if not text:
        raise ValueError("duration is empty")

    seconds = 0
    seen = set()
    last_index = None
    i = 0
    n = len(text)

    while i < n:
        start = i
        number = ""
        while i < n and text[i].isdigit():
            number += text[i]
            i += 1
        if not number:
            raise ValueError(f"expected a number at position {start} in {text!r}")
        value = int(number)

        unit_index = None
        for unit in _ORDER:
            if text.startswith(unit, i):
                unit_index = _UNITS[unit]
                i += len(unit)
                break
        if unit_index is None:
            raise ValueError(f"expected a unit at position {i} in {text!r}")
        if unit_index in seen:
            raise ValueError(f"unit repeated in {text!r}")
        seen.add(unit_index)
        if last_index is not None and unit_index >= last_index:
            raise ValueError(f"units not in descending order in {text!r}")
        last_index = unit_index

        seconds += value * unit_index

    result = -seconds if negative else seconds
    return result


def format_duration(seconds: int) -> str:
    """Format whole seconds as a canonical compact duration string."""
    if seconds == 0:
        return "0s"

    negative = seconds < 0
    total = abs(seconds)

    parts = []
    for unit in _ORDER:
        factor = _UNITS[unit]
        if total >= factor:
            count, total = divmod(total, factor)
            parts.append(f"{count}{unit}")

    result = "".join(parts)
    return "-" + result if negative else result
