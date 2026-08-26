import statistics


def median(numbers: list) -> float:
    """Return the statistical median of a non-empty list."""
    if not numbers:
        raise ValueError("median() requires a non-empty list")
    return statistics.median(numbers)


def variance(numbers: list, sample: bool = True) -> float:
    """Return the sample (n-1) or population (n) variance of a sequence.

    Uses the two-pass mean-then-squared-deviations formulation. The input is
    not mutated. An empty sequence raises for either mode; a single-element
    sequence raises for sample variance and returns 0.0 for population.
    """
    if not numbers:
        raise ValueError("variance() requires a non-empty list")
    length = len(numbers)
    if sample and length < 2:
        raise ValueError("sample variance requires at least two elements")
    mean = sum(numbers) / length
    total = 0.0
    for number in numbers:
        total += (number - mean) ** 2
    if sample:
        return total / (length - 1)
    return total / length


def mode(numbers: list):
    """Return the most frequent value, ties broken by first appearance."""
    if not numbers:
        raise ValueError("mode() requires a non-empty list")
    counts = {}
    first = {}
    for index, number in enumerate(numbers):
        counts[number] = counts.get(number, 0) + 1
        first.setdefault(number, index)
    return max(counts, key=lambda n: (counts[n], -first[n]))


def percentile(numbers, p):
    """Return the p-th percentile of a non-empty sequence.

    Uses linear interpolation between closest ranks (numpy 'linear' method).
    p must be in [0, 100]. Returns the minimum at p=0 and the maximum at p=100.
    The input is not mutated.
    """
    if not numbers:
        raise ValueError("percentile() requires a non-empty sequence")
    if not (0 <= p <= 100):
        raise ValueError("percentile() requires 0 <= p <= 100")
    sorted_numbers = sorted(numbers)
    if len(sorted_numbers) == 1:
        return sorted_numbers[0]
    rank = (p / 100.0) * (len(sorted_numbers) - 1)
    floor_index = int(rank)
    ceil_index = floor_index + 1
    if ceil_index >= len(sorted_numbers):
        return sorted_numbers[-1]
    if rank == floor_index:
        return sorted_numbers[floor_index]
    fraction = rank - floor_index
    low = sorted_numbers[floor_index]
    high = sorted_numbers[ceil_index]
    return low + (high - low) * fraction
