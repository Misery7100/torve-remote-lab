import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.stats import percentile


class PercentileTest(unittest.TestCase):
    def test_empty_raises_valueerror(self):
        with self.assertRaises(ValueError):
            percentile([], 50)

    def test_p_below_zero_raises_valueerror(self):
        with self.assertRaises(ValueError):
            percentile([1, 2, 3], -1)

    def test_p_above_100_raises_valueerror(self):
        with self.assertRaises(ValueError):
            percentile([1, 2, 3], 101)

    def test_single_element(self):
        self.assertEqual(percentile([5], 0), 5)
        self.assertEqual(percentile([5], 42), 5)
        self.assertEqual(percentile([5], 100), 5)

    def test_p_zero_returns_minimum(self):
        self.assertEqual(percentile([3, 1, 2], 0), 1)

    def test_p_100_returns_maximum(self):
        self.assertEqual(percentile([3, 1, 2], 100), 3)

    def test_median_interpolation(self):
        self.assertAlmostEqual(percentile([1, 2, 3], 50), 2.0)

    def test_interpolation_midpoint(self):
        self.assertEqual(percentile([1, 2], 50), 1.5)

    def test_interpolation_fractional(self):
        self.assertAlmostEqual(percentile([1, 2, 3, 4], 25), 1.75)

    def test_unsorted_input(self):
        self.assertAlmostEqual(percentile([4, 1, 3, 2], 25), 1.75)

    def test_input_not_mutated(self):
        numbers = [4, 1, 3, 2, 5]
        original = list(numbers)
        percentile(numbers, 50)
        self.assertEqual(numbers, original)


if __name__ == "__main__":
    unittest.main()
