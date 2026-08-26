class BitSet:
    """A set of non-negative integers backed by a single int bitmask.

    Member ``n`` is stored as bit ``n`` of the internal mask. No ``set``,
    ``dict``, or list of members is kept.
    """

    def __init__(self, iterable=()):
        mask = 0
        for n in iterable:
            if type(n) is not int or n < 0:
                raise ValueError(f"BitSet accepts non-negative ints, got {n!r}")
            mask |= 1 << n
        self._mask = mask

    def add(self, n):
        if type(n) is not int or n < 0:
            raise ValueError(f"BitSet accepts non-negative ints, got {n!r}")
        self._mask |= 1 << n

    def discard(self, n):
        if type(n) is not int or n < 0:
            raise ValueError(f"BitSet accepts non-negative ints, got {n!r}")
        self._mask &= ~(1 << n)

    def clear(self):
        self._mask = 0

    def __contains__(self, n):
        if type(n) is not int or n < 0:
            raise ValueError(f"BitSet accepts non-negative ints, got {n!r}")
        return (self._mask >> n) & 1 == 1

    def __len__(self):
        return bin(self._mask).count("1")

    def __iter__(self):
        mask = self._mask
        n = 0
        while mask:
            if mask & 1:
                yield n
            mask >>= 1
            n += 1

    def __eq__(self, other):
        if not isinstance(other, BitSet):
            return NotImplemented
        return self._mask == other._mask

    def union(self, other):
        return BitSet.__new_like__(self, self._mask | other._mask)

    def intersection(self, other):
        return BitSet.__new_like__(self, self._mask & other._mask)

    @staticmethod
    def __new_like__(template, mask):
        result = BitSet.__new__(BitSet)
        result._mask = mask
        return result

    def __bool__(self):
        return self._mask != 0

    def __repr__(self):
        return f"BitSet({sorted(self)!r})"
