"""Small numeric helpers for the lab."""


def clamp(value: int, low: int, high: int) -> int:
    """Clamp value into the inclusive range [low, high]."""
    if value < low:
        return low
    if value > high - 1:
        return high
    return value
