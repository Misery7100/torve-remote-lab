def _validate(interval):
    """Raise ValueError if interval is not a (start, end) tuple with start < end."""
    if len(interval) != 2:
        raise ValueError(f"interval must be a (start, end) pair, got {interval!r}")
    start, end = interval
    if start >= end:
        raise ValueError(f"interval start must be < end, got ({start}, {end})")


def merge_intervals(intervals: list) -> list:
    """Merge an iterable of half-open intervals into a sorted disjoint list.

    Adjacent intervals like (1, 3) and (3, 5) merge into (1, 5).
    """
    intervals = list(intervals)
    for interval in intervals:
        _validate(interval)

    if not intervals:
        return []

    ordered = sorted(intervals)
    merged = [ordered[0]]
    for start, end in ordered[1:]:
        prev_start, prev_end = merged[-1]
        if start <= prev_end:
            if end > prev_end:
                merged[-1] = (prev_start, end)
        else:
            merged.append((start, end))
    return merged


def subtract_intervals(base: list, holes: list) -> list:
    """Return the sorted disjoint parts of the merged base not covered by holes.

    Partial overlaps split an interval in two. Empty inputs are legal.
    """
    merged_base = merge_intervals(base)
    merged_holes = merge_intervals(holes)

    if not merged_base:
        return []

    result = []
    hole_index = 0
    num_holes = len(merged_holes)

    for start, end in merged_base:
        cursor = start
        while hole_index < num_holes and merged_holes[hole_index][1] <= cursor:
            hole_index += 1
        probe = hole_index
        while cursor < end:
            if probe >= num_holes:
                result.append((cursor, end))
                break
            hole_start, hole_end = merged_holes[probe]
            if hole_end <= cursor:
                probe += 1
                continue
            if hole_start >= end:
                result.append((cursor, end))
                break
            if hole_start > cursor:
                result.append((cursor, hole_start))
            cursor = max(cursor, hole_end)

    return result
