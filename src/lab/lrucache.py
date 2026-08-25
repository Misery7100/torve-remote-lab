import time
from collections import OrderedDict


class LRUCache:
    """A fixed-capacity least-recently-used cache with optional per-entry TTLs.

    max_size is a positive integer bounding the number of live (unexpired)
    entries. When the cache is full, inserting a new key evicts the least
    recently used unexpired entry first.

    Each entry carries its own TTL in seconds. An entry's TTL is fixed at write
    time (either its own ttl argument or the cache's default) and it expires
    once the injected clock has advanced past the write time plus the TTL.
    Expired entries are treated as absent and evicted lazily on access, and are
    never returned even if the clock jumps far forward.

    All timing uses the injectable clock, defaulting to time.monotonic, so
    callers may substitute a fake clock in tests.
    """

    def __init__(self, max_size, ttl=None, clock=time.monotonic):
        if not isinstance(max_size, int) or max_size <= 0:
            raise ValueError("max_size must be a positive integer")
        if ttl is not None and (not isinstance(ttl, (int, float)) or ttl <= 0):
            raise ValueError("ttl must be a positive number or None")
        self.max_size = max_size
        self._default_ttl = ttl
        self._clock = clock
        self._data = OrderedDict()

    def put(self, key, value, ttl=None):
        if ttl is not None and (not isinstance(ttl, (int, float)) or ttl <= 0):
            raise ValueError("ttl must be a positive number or None")
        entry_ttl = self._default_ttl if ttl is None else ttl
        now = self._clock()
        if entry_ttl is None:
            expires_at = None
        else:
            expires_at = now + entry_ttl
        self._data[key] = (value, expires_at)
        self._data.move_to_end(key)
        self._evict(now)

    def get(self, key, default=None):
        now = self._clock()
        if key not in self._data:
            return default
        value, expires_at = self._data[key]
        if expires_at is not None and now >= expires_at:
            del self._data[key]
            return default
        self._data.move_to_end(key)
        return value

    def contains(self, key):
        now = self._clock()
        if key not in self._data:
            return False
        value, expires_at = self._data[key]
        if expires_at is not None and now >= expires_at:
            del self._data[key]
            return False
        return True

    def __len__(self):
        now = self._clock()
        expired = [
            key for key, (_, expires_at) in self._data.items()
            if expires_at is not None and now >= expires_at
        ]
        for key in expired:
            del self._data[key]
        return len(self._data)

    def _evict(self, now):
        while len(self._data) > self.max_size:
            for key in list(self._data.keys()):
                value, expires_at = self._data[key]
                if expires_at is not None and now >= expires_at:
                    del self._data[key]
                    continue
                self._data.popitem(last=False)
                break
