class RangeSet:
    """A sorted set of non-overlapping half-open integer ranges.

    The internal ``_ranges`` list holds disjoint ``(start, stop)`` tuples in
    ascending order. ``add`` inserts a range, merging any overlapping or
    adjacent (``stop == next.start``) ranges; ``contains`` answers membership;
    ``ranges`` returns the normalized ascending list of ``(start, stop)``
    tuples; ``total`` returns the count of covered integers.
    """

    def __init__(self):
        self._ranges = []

    def _validate(self, start, stop):
        if stop <= start:
            raise ValueError(f"stop must be > start, got ({start}, {stop})")

    def add(self, start, stop):
        """Insert the half-open range [start, stop), merging as needed."""
        self._validate(start, stop)
        ranges = self._ranges

        new_start = start
        new_stop = stop
        i = 0
        n = len(ranges)

        while i < n and ranges[i][1] < new_start:
            i += 1

        while i < n and ranges[i][0] <= new_stop:
            old_start, old_stop = ranges[i]
            if old_start < new_start:
                new_start = old_start
            if old_stop > new_stop:
                new_stop = old_stop
            del ranges[i]
            n -= 1

        ranges.insert(i, (new_start, new_stop))

    def contains(self, n):
        """Return True if integer n is covered by this set."""
        lo, hi = 0, len(self._ranges)
        while lo < hi:
            mid = (lo + hi) // 2
            start, stop = self._ranges[mid]
            if n < start:
                hi = mid
            elif n >= stop:
                lo = mid + 1
            else:
                return True
        return False

    def ranges(self):
        """Return the normalized ascending list of (start, stop) tuples."""
        return list(self._ranges)

    def total(self):
        """Return the number of covered integers."""
        return sum(stop - start for start, stop in self._ranges)
