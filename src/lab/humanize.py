"""Human-readable byte counts and compact durations."""


def format_bytes(count: int) -> str:
    """Format a non-negative integer byte count using binary (1024) units.

    Values below one KiB stay whole ('512 B'). Larger counts use one decimal
    place, dropping a trailing '.0' ('1536' -> '1.5 KiB', '2048' -> '2 KiB').
    Raises ValueError when count is negative or not an integer.
    """
    if not isinstance(count, int) or count < 0:
        raise ValueError(f"count must be a non-negative integer, got {count!r}")

    units = [
        ("EiB", 1024 ** 6),
        ("PiB", 1024 ** 5),
        ("TiB", 1024 ** 4),
        ("GiB", 1024 ** 3),
        ("MiB", 1024 ** 2),
        ("KiB", 1024),
    ]
    for label, factor in units:
        if count >= factor:
            value = count / factor
            text = f"{value:.1f}"
            if text.endswith(".0"):
                text = text[:-2]
            return f"{text} {label}"
    return f"{count} B"


def format_seconds(seconds: int) -> str:
    """Format a non-negative whole-second count as a compact duration string.

    Zero-valued components are omitted ('3661' -> '1h 1m 1s') and zero itself
    renders as '0s'. Raises ValueError when seconds is negative or not an
    integer.
    """
    if not isinstance(seconds, int) or seconds < 0:
        raise ValueError(f"seconds must be a non-negative integer, got {seconds!r}")

    if seconds == 0:
        return "0s"

    parts = []
    for unit, factor in (("h", 3600), ("m", 60), ("s", 1)):
        count, seconds = divmod(seconds, factor)
        if count:
            parts.append(f"{count}{unit}")
    return " ".join(parts)
