import statistics


def median(numbers: list) -> float:
    """Return the statistical median of a non-empty list."""
    if not numbers:
        raise ValueError("median() requires a non-empty list")
    return statistics.median(numbers)


def variance(numbers: list) -> float:
    """Return the population variance of a non-empty list."""
    if not numbers:
        raise ValueError("variance() requires a non-empty list")
    return statistics.pvariance(numbers)
