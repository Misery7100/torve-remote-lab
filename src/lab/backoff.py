import functools
import random
import time


def retry(max_attempts=3, base_delay=0.1, max_delay=10.0, retry_on=(Exception,), sleeper=time.sleep, rng=random.random):
    """Retry a function with full-jitter exponential backoff on failure."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while True:
                try:
                    return func(*args, **kwargs)
                except retry_on:
                    if attempt >= max_attempts:
                        raise
                    cap = min(max_delay, base_delay * 2 ** (attempt - 1))
                    sleeper(rng() * cap)
                    attempt += 1

        return wrapper

    return decorator
