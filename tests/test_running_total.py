import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import running_total


class RunningTotalTest(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(running_total([]), [])

    def test_single_number(self):
        self.assertEqual(running_total([5]), [5])

    def test_positive_numbers(self):
        self.assertEqual(running_total([1, 2, 3]), [1, 3, 6])

    def test_negative_numbers(self):
        self.assertEqual(running_total([1, -2, 3]), [1, -1, 2])

    def test_zero(self):
        self.assertEqual(running_total([0, 0, 0]), [0, 0, 0])

    def test_accumulates_expected_running_sum(self):
        self.assertEqual(running_total([1, 1, 1, 1]), [1, 2, 3, 4])


if __name__ == "__main__":
    unittest.main()
