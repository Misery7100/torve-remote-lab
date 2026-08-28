import heapq


class MedianTracker:
    """Track the running median of a live numeric stream in O(log n) per value.

    Values are kept split into two heaps: a max-heap for the lower half and a
    min-heap for the upper half. Each insertion is balanced so the halves
    differ in size by at most one, keeping the median reachable in O(1) from
    the heap roots.
    """

    def __init__(self):
        # Lower half (values <= upper half) stored as a max-heap: heapq keeps
        # the minimum at index 0, so negatives invert that into a max-heap.
        self._lower = []  # inv: holds the smaller values, root is the max
        # Upper half stored as a regular min-heap.
        self._upper = []  # inv: holds the larger values, root is the min

    def add(self, x):
        """Insert a value into the tracker."""
        if not self._lower or x <= -self._lower[0]:
            heapq.heappush(self._lower, -x)
        else:
            heapq.heappush(self._upper, x)
        self._rebalance()

    def median(self):
        """Return the median of all added values.

        For an even count this is the mean of the two middle values. Raises
        ValueError when no value has been added yet.
        """
        if not self._lower:
            raise ValueError("median() called on an empty MedianTracker")
        if len(self._lower) > len(self._upper):
            return -self._lower[0]
        if len(self._upper) > len(self._lower):
            return self._upper[0]
        return (-self._lower[0] + self._upper[0]) / 2

    def count(self):
        """Return how many values have been added."""
        return len(self._lower) + len(self._upper)

    def _rebalance(self):
        """Restore the invariant that the halves differ in size by at most one."""
        while len(self._lower) > len(self._upper) + 1:
            heapq.heappush(self._upper, -heapq.heappop(self._lower))
        while len(self._upper) > len(self._lower):
            heapq.heappush(self._lower, -heapq.heappop(self._upper))
