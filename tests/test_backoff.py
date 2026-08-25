import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.backoff import retry


class RecordingSleep:
    def __init__(self):
        self.calls = []

    def __call__(self, delay):
        self.calls.append(delay)


class FixedRandom:
    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value


class RetryTest(unittest.TestCase):
    def test_success_passthrough(self):
        sleeper = RecordingSleep()
        calls = []

        @retry(max_attempts=3, sleeper=sleeper, rng=FixedRandom(1.0))
        def func():
            calls.append(1)
            return "ok"

        result = func()
        self.assertEqual(result, "ok")
        self.assertEqual(calls, [1])
        self.assertEqual(sleeper.calls, [])

    def test_value_return_passes_through(self):
        sleeper = RecordingSleep()

        @retry(max_attempts=3, sleeper=sleeper, rng=FixedRandom(1.0))
        def func():
            return 42

        self.assertEqual(func(), 42)
        self.assertEqual(sleeper.calls, [])

    def test_retry_then_succeed(self):
        sleeper = RecordingSleep()
        calls = []

        @retry(max_attempts=5, base_delay=1.0, sleeper=sleeper, rng=FixedRandom(0.5))
        def func():
            calls.append(1)
            if len(calls) < 3:
                raise ValueError("boom")
            return "done"

        result = func()
        self.assertEqual(result, "done")
        self.assertEqual(len(calls), 3)
        # two sleeps recorded
        self.assertEqual(sleeper.calls, [0.5, 1.0])

    def test_exhaustion_re_raises_last_exception(self):
        sleeper = RecordingSleep()

        @retry(max_attempts=3, base_delay=1.0, sleeper=sleeper, rng=FixedRandom(1.0))
        def func():
            raise KeyError("x")

        with self.assertRaises(KeyError):
            func()
        self.assertEqual(len(sleeper.calls), 2)

    def test_re_raise_preserves_traceback(self):
        sleeper = RecordingSleep()

        @retry(max_attempts=2, sleeper=sleeper, rng=FixedRandom(1.0))
        def func():
            raise ValueError("boom")

        try:
            func()
        except ValueError as exc:
            import traceback

            tb = traceback.extract_tb(exc.__traceback__)
            self.assertTrue(any(line.name == "func" for line in tb))

    def test_non_matching_exception_propagates_first_call(self):
        sleeper = RecordingSleep()

        @retry(max_attempts=3, retry_on=ValueError, sleeper=sleeper, rng=FixedRandom(1.0))
        def func():
            raise TypeError("not retried")

        with self.assertRaises(TypeError):
            func()
        self.assertEqual(sleeper.calls, [])

    def test_retry_on_multiple_types(self):
        sleeper = RecordingSleep()

        @retry(max_attempts=3, retry_on=(ValueError, KeyError), sleeper=sleeper, rng=FixedRandom(1.0))
        def func():
            raise KeyError("retried")

        with self.assertRaises(KeyError):
            func()
        self.assertEqual(len(sleeper.calls), 2)

    def test_default_retry_on_exception(self):
        sleeper = RecordingSleep()

        @retry(max_attempts=2, sleeper=sleeper, rng=FixedRandom(1.0))
        def func():
            raise RuntimeError("x")

        with self.assertRaises(RuntimeError):
            func()
        self.assertEqual(len(sleeper.calls), 1)

    def test_jitter_bounded_by_cap(self):
        sleeper = RecordingSleep()
        calls = []

        def func():
            calls.append(1)
            raise ValueError("boom")

        func = retry(max_attempts=3, base_delay=1.0, max_delay=1.5, sleeper=sleeper, rng=FixedRandom(1.0))(func)

        with self.assertRaises(ValueError):
            func()

        expected_caps = [1.0, 2.0]
        for delay, cap in zip(sleeper.calls, expected_caps):
            self.assertGreaterEqual(delay, 0.0)
            self.assertLessEqual(delay, min(1.5, cap))
        self.assertLessEqual(max(sleeper.calls), 1.5)

    def test_jitter_never_exceeds_capped_upper_bound(self):
        sleeper = RecordingSleep()

        @retry(max_attempts=4, base_delay=2.0, max_delay=3.0, sleeper=sleeper, rng=FixedRandom(1.0))
        def func():
            raise RuntimeError("x")

        with self.assertRaises(RuntimeError):
            func()

        for delay in sleeper.calls:
            self.assertLessEqual(delay, 3.0)

    def test_zero_delay_when_rng_zero(self):
        sleeper = RecordingSleep()

        @retry(max_attempts=3, base_delay=2.0, sleeper=sleeper, rng=FixedRandom(0.0))
        def func():
            raise RuntimeError("x")

        with self.assertRaises(RuntimeError):
            func()

        self.assertEqual(sleeper.calls, [0.0, 0.0])

    def test_recorded_sleep_counts(self):
        sleeper = RecordingSleep()

        @retry(max_attempts=4, sleeper=sleeper, rng=FixedRandom(1.0))
        def func():
            raise ValueError("x")

        with self.assertRaises(ValueError):
            func()

        # 4 attempts -> 3 sleeps before exhausting
        self.assertEqual(len(sleeper.calls), 3)

    def test_max_attempts_less_than_one_raises(self):
        with self.assertRaises(ValueError):
            retry(max_attempts=0)
        with self.assertRaises(ValueError):
            retry(max_attempts=-1)

    def test_max_attempts_one_no_sleep(self):
        sleeper = RecordingSleep()

        @retry(max_attempts=1, sleeper=sleeper, rng=FixedRandom(1.0))
        def func():
            raise ValueError("x")

        with self.assertRaises(ValueError):
            func()
        self.assertEqual(sleeper.calls, [])

    def test_wraps_preserves_metadata(self):
        def original():
            """Docstring here."""

        wrapped = retry()(original)
        self.assertEqual(wrapped.__name__, "original")
        self.assertEqual(wrapped.__doc__, "Docstring here.")

    def test_no_real_sleeping_under_test(self):
        # a sleeper that would fail loudly if called with a real duration
        class ExplodingSleep:
            def __init__(self):
                self.calls = []

            def __call__(self, delay):
                self.calls.append(delay)

        sleeper = ExplodingSleep()

        @retry(max_attempts=3, sleeper=sleeper, rng=FixedRandom(0.1))
        def func():
            raise ValueError("x")

        with self.assertRaises(ValueError):
            func()
        self.assertTrue(all(0.0 <= d for d in sleeper.calls))
        self.assertEqual(len(sleeper.calls), 2)


if __name__ == "__main__":
    unittest.main()
