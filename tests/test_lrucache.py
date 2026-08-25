import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.lrucache import LRUCache


class FakeClock:
    def __init__(self, start=0.0):
        self.now = start

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


class CacheConstructionTest(unittest.TestCase):
    def test_default_clock_is_monotonic(self):
        cache = LRUCache(2)
        self.assertIs(cache._clock, __import__("time").monotonic)

    def test_zero_max_size_raises(self):
        with self.assertRaises(ValueError):
            LRUCache(0)

    def test_negative_max_size_raises(self):
        with self.assertRaises(ValueError):
            LRUCache(-1)

    def test_non_positive_default_ttl_raises(self):
        with self.assertRaises(ValueError):
            LRUCache(2, ttl=0)
        with self.assertRaises(ValueError):
            LRUCache(2, ttl=-5)


class RecencyEvictionOrderTest(unittest.TestCase):
    def test_evicts_least_recently_used_unexpired_entry_on_overflow(self):
        clock = FakeClock()
        cache = LRUCache(2, clock=clock)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        self.assertEqual(cache.get("a"), None)
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)

    def test_get_refreshes_recency(self):
        clock = FakeClock()
        cache = LRUCache(2, clock=clock)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")
        cache.put("c", 3)
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("b"), None)
        self.assertEqual(cache.get("c"), 3)

    def test_new_put_evicts_oldest(self):
        clock = FakeClock()
        cache = LRUCache(2, clock=clock)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        self.assertEqual(cache.get("a"), None)
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)


class TtlExpiryTest(unittest.TestCase):
    def test_expired_entry_not_returned_after_clock_jumps(self):
        clock = FakeClock()
        cache = LRUCache(2, ttl=10, clock=clock)
        cache.put("a", 1)
        clock.advance(1000)
        self.assertEqual(cache.get("a"), None)

    def test_expired_entry_evicted_lazily_by_get(self):
        clock = FakeClock()
        cache = LRUCache(2, ttl=10, clock=clock)
        cache.put("a", 1)
        cache.put("b", 2)
        clock.advance(20)
        cache.get("a")
        cache.put("c", 3)
        self.assertEqual(cache.get("a"), None)
        self.assertEqual(cache.get("b"), None)
        self.assertEqual(cache.get("c"), 3)

    def test_unexpired_entry_returned_within_ttl(self):
        clock = FakeClock()
        cache = LRUCache(2, ttl=10, clock=clock)
        cache.put("a", 1)
        clock.advance(9.999)
        self.assertEqual(cache.get("a"), 1)

    def test_entry_expired_at_ttl_boundary(self):
        clock = FakeClock()
        cache = LRUCache(2, ttl=10, clock=clock)
        cache.put("a", 1)
        clock.advance(10)
        self.assertEqual(cache.get("a"), None)


class PerEntryTtlOverrideTest(unittest.TestCase):
    def test_entry_ttl_overrides_default(self):
        clock = FakeClock()
        cache = LRUCache(2, ttl=100, clock=clock)
        cache.put("a", 1, ttl=5)
        cache.put("b", 2)
        clock.advance(6)
        self.assertEqual(cache.get("a"), None)
        self.assertEqual(cache.get("b"), 2)

    def test_default_used_without_entry_ttl(self):
        clock = FakeClock()
        cache = LRUCache(2, ttl=5, clock=clock)
        cache.put("a", 1)
        clock.advance(6)
        self.assertEqual(cache.get("a"), None)

    def test_no_default_ttl_is_persistent(self):
        clock = FakeClock()
        cache = LRUCache(2, clock=clock)
        cache.put("a", 1)
        clock.advance(1000)
        self.assertEqual(cache.get("a"), 1)


class LenSemanticsTest(unittest.TestCase):
    def test_len_counts_only_unexpired_entries(self):
        clock = FakeClock()
        cache = LRUCache(3, ttl=10, clock=clock)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        clock.advance(20)
        self.assertEqual(len(cache), 0)

    def test_len_removes_expired_entries(self):
        clock = FakeClock()
        cache = LRUCache(3, ttl=10, clock=clock)
        cache.put("a", 1, ttl=5)
        cache.put("b", 2)
        cache.put("c", 3)
        clock.advance(6)
        self.assertEqual(len(cache), 2)
        self.assertEqual(cache.get("a"), None)
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)


class UpdateRefreshesRecencyTest(unittest.TestCase):
    def test_put_updates_value_and_recency(self):
        clock = FakeClock()
        cache = LRUCache(2, clock=clock)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("a", 100)
        cache.put("c", 3)
        self.assertEqual(cache.get("a"), 100)
        self.assertEqual(cache.get("b"), None)
        self.assertEqual(cache.get("c"), 3)

    def test_put_updates_ttl(self):
        clock = FakeClock()
        cache = LRUCache(2, ttl=10, clock=clock)
        cache.put("a", 1)
        cache.put("a", 2, ttl=100)
        clock.advance(50)
        self.assertEqual(cache.get("a"), 2)


class ContainsTest(unittest.TestCase):
    def test_contains_checks_without_refreshing_recency(self):
        clock = FakeClock()
        cache = LRUCache(2, clock=clock)
        cache.put("a", 1)
        cache.put("b", 2)
        self.assertTrue(cache.contains("a"))
        cache.put("c", 3)
        self.assertEqual(cache.get("a"), None)
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)

    def test_contains_false_for_expired(self):
        clock = FakeClock()
        cache = LRUCache(2, ttl=10, clock=clock)
        cache.put("a", 1)
        clock.advance(20)
        self.assertFalse(cache.contains("a"))

    def test_contains_false_for_missing(self):
        clock = FakeClock()
        cache = LRUCache(2, clock=clock)
        self.assertFalse(cache.contains("missing"))


if __name__ == "__main__":
    unittest.main()
