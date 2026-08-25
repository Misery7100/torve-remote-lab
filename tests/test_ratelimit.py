import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.ratelimit import RateLimiter


class FakeClock:
    def __init__(self, start=0.0):
        self.time = start

    def __call__(self):
        return self.time

    def advance(self, seconds):
        self.time += seconds


class RateLimiterInitTest(unittest.TestCase):
    def test_non_positive_capacity_raises_valueerror(self):
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                RateLimiter(bad, 1.0)

    def test_non_positive_refill_rate_raises_valueerror(self):
        for bad in (0, -1.0):
            with self.assertRaises(ValueError):
                RateLimiter(1, bad)


class BurstDrainTest(unittest.TestCase):
    def test_burst_drains_full_capacity(self):
        clock = FakeClock()
        limiter = RateLimiter(5, 1.0, clock=clock)
        for _ in range(5):
            self.assertTrue(limiter.allow())
        self.assertFalse(limiter.allow())

    def test_partial_allow_consumes_remaining(self):
        clock = FakeClock()
        limiter = RateLimiter(3, 1.0, clock=clock)
        self.assertTrue(limiter.allow(2))
        self.assertTrue(limiter.allow(1))
        self.assertFalse(limiter.allow(1))

    def test_cost_greater_than_capacity_raises_valueerror(self):
        clock = FakeClock()
        limiter = RateLimiter(2, 1.0, clock=clock)
        with self.assertRaises(ValueError):
            limiter.allow(3)
        with self.assertRaises(ValueError):
            limiter.allow(0)


class RefillOverTimeTest(unittest.TestCase):
    def test_refills_over_time(self):
        clock = FakeClock()
        limiter = RateLimiter(10, 2.0, clock=clock)
        for _ in range(10):
            limiter.allow()
        self.assertFalse(limiter.allow())
        clock.advance(1.0)
        self.assertTrue(limiter.allow(2))
        self.assertFalse(limiter.allow())

    def test_wait_time_reflects_refill(self):
        clock = FakeClock()
        limiter = RateLimiter(1, 4.0, clock=clock)
        self.assertTrue(limiter.allow())
        self.assertAlmostEqual(limiter.wait_time(1), 0.25)
        self.assertEqual(limiter.wait_time(), 0.25)
        clock.advance(0.25)
        self.assertEqual(limiter.wait_time(), 0.0)

    def test_wait_time_zero_when_allowed(self):
        clock = FakeClock()
        limiter = RateLimiter(3, 5.0, clock=clock)
        self.assertEqual(limiter.wait_time(), 0.0)
        self.assertEqual(limiter.wait_time(3), 0.0)

    def test_wait_time_partial_tokens(self):
        clock = FakeClock()
        limiter = RateLimiter(10, 1.0, clock=clock)
        limiter.allow(7)
        self.assertAlmostEqual(limiter.wait_time(10), 7.0)


class CapAtCapacityTest(unittest.TestCase):
    def test_tokens_never_exceed_capacity(self):
        clock = FakeClock()
        limiter = RateLimiter(3, 10.0, clock=clock)
        self.assertTrue(limiter.allow(3))
        clock.advance(100.0)
        self.assertEqual(limiter.wait_time(3), 0.0)
        self.assertTrue(limiter.allow(3))
        self.assertFalse(limiter.allow(1))


class BackwardsClockTest(unittest.TestCase):
    def test_backwards_clock_mints_no_tokens(self):
        clock = FakeClock(10.0)
        limiter = RateLimiter(2, 1.0, clock=clock)
        self.assertTrue(limiter.allow(2))
        self.assertFalse(limiter.allow())
        clock.time = 5.0
        self.assertEqual(limiter.wait_time(1), 1.0)
        self.assertFalse(limiter.allow())
        clock.time = 15.0
        self.assertTrue(limiter.allow(1))

    def test_regression_and_recovery_accrue_no_phantom_tokens(self):
        clock = FakeClock(10.0)
        limiter = RateLimiter(2, 1.0, clock=clock)
        self.assertTrue(limiter.allow(2))
        self.assertFalse(limiter.allow())
        clock.time = 5.0
        self.assertEqual(limiter.wait_time(1), 1.0)
        self.assertFalse(limiter.allow())
        clock.time = 10.0
        self.assertEqual(limiter.wait_time(1), 1.0)
        self.assertFalse(limiter.allow())
        clock.time = 11.0
        self.assertTrue(limiter.allow(1))
        self.assertFalse(limiter.allow())


class CostValidationTest(unittest.TestCase):
    def test_non_positive_cost_raises_valueerror(self):
        clock = FakeClock()
        limiter = RateLimiter(5, 1.0, clock=clock)
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                limiter.allow(bad)
            with self.assertRaises(ValueError):
                limiter.wait_time(bad)

    def test_cost_above_capacity_raises_valueerror(self):
        clock = FakeClock()
        limiter = RateLimiter(4, 1.0, clock=clock)
        with self.assertRaises(ValueError):
            limiter.allow(5)
        with self.assertRaises(ValueError):
            limiter.wait_time(5)


if __name__ == "__main__":
    unittest.main()
