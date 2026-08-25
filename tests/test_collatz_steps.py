import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import collatz_steps


class CollatzStepsTest(unittest.TestCase):
    def test_one_takes_zero_steps(self):
        self.assertEqual(collatz_steps(1), 0)

    def test_two_takes_one_step(self):
        self.assertEqual(collatz_steps(2), 1)

    def test_three_takes_seven_steps(self):
        self.assertEqual(collatz_steps(3), 7)

    def test_four_takes_two_steps(self):
        self.assertEqual(collatz_steps(4), 2)

    def test_even_power_of_two(self):
        self.assertEqual(collatz_steps(1024), 10)

    def test_larger_number(self):
        self.assertEqual(collatz_steps(27), 111)

    def test_raises_for_zero(self):
        with self.assertRaises(ValueError):
            collatz_steps(0)

    def test_raises_for_negative(self):
        with self.assertRaises(ValueError):
            collatz_steps(-5)


if __name__ == "__main__":
    unittest.main()
