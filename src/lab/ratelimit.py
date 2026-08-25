import time


class RateLimiter:
    """A token-bucket rate limiter with continuous refill.

    Tokens accrue continuously (fractionally) between calls up to `capacity`.
    `allow` consumes tokens without blocking; `wait_time` reports the delay
    until enough tokens accrue.
    """

    def __init__(self, capacity: int, refill_rate: float, clock=time.monotonic):
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        if refill_rate <= 0:
            raise ValueError("refill_rate must be > 0")
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._clock = clock
        self._tokens = float(capacity)
        self._last = clock()

    def _refill(self):
        now = self._clock()
        elapsed = now - self._last
        if elapsed > 0:
            self._tokens = min(self.capacity, self._tokens + elapsed * self.refill_rate)
            self._last = now
        else:
            self._last = now

    def allow(self, cost: int = 1) -> bool:
        if cost <= 0:
            raise ValueError("cost must be > 0")
        if self.capacity < cost:
            raise ValueError("cost exceeds capacity")
        self._refill()
        if self._tokens >= cost:
            self._tokens -= cost
            return True
        return False

    def wait_time(self, cost: int = 1) -> float:
        if cost <= 0:
            raise ValueError("cost must be > 0")
        if self.capacity < cost:
            raise ValueError("cost exceeds capacity")
        self._refill()
        if self._tokens >= cost:
            return 0.0
        return (cost - self._tokens) / self.refill_rate
