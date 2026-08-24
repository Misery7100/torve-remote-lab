import statistics


def median(numbers: list) -> float:
    """Return the statistical median of a non-empty list."""
    if not numbers:
        raise ValueError("median() requires a non-empty list")
    return statistics.median(numbers)


def mode(numbers: list):
    """Return the most frequent value; ties broken by first appearance."""
    if not numbers:
        raise ValueError("mode() requires a non-empty list")
    counts = {}
    first = {}
    for index, number in enumerate(numbers):
        counts[number] = counts.get(number, 0) + 1
        first.setdefault(number, index)
    return max(counts, key=lambda n: (counts[n], -first[n]))
