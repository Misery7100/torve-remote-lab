import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.stats import median


class MedianTest(unittest.TestCase):
    def test_empty_raises_valueerror(self):
        with self.assertRaises(ValueError):
            median([])

    def test_single_element(self):
        self.assertEqual(median([5]), 5)

    def test_odd_length_unsorted(self):
        self.assertEqual(median([3, 1, 2]), 2)

    def test_even_length_returns_average(self):
        self.assertEqual(median([1, 2, 3, 4]), 2.5)

    def test_negative_numbers(self):
        self.assertEqual(median([-3, -1, -2]), -2)

    def test_floats(self):
        self.assertEqual(median([1.5, 2.5]), 2.0)


if __name__ == "__main__":
    unittest.main()
