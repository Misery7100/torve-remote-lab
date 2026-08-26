import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.stats import median, mode, variance


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


class VarianceTest(unittest.TestCase):
    def test_empty_raises_valueerror(self):
        with self.assertRaises(ValueError):
            variance([])
        with self.assertRaises(ValueError):
            variance([], sample=False)

    def test_single_element_population(self):
        self.assertEqual(variance([5], sample=False), 0)

    def test_identical_values(self):
        self.assertEqual(variance([3, 3, 3, 3], sample=False), 0)

    def test_two_elements(self):
        self.assertEqual(variance([2, 4], sample=False), 1)

    def test_known_population(self):
        self.assertEqual(variance([1, 2, 3, 4, 5], sample=False), 2)

    def test_negative_and_positive(self):
        self.assertEqual(variance([-2, 2], sample=False), 4)


class ModeTest(unittest.TestCase):
    def test_empty_raises_valueerror(self):
        with self.assertRaises(ValueError):
            mode([])

    def test_single_element(self):
        self.assertEqual(mode([5]), 5)

    def test_single_mode(self):
        self.assertEqual(mode([1, 2, 2, 3]), 2)

    def test_tie_broken_by_first_appearance(self):
        self.assertEqual(mode([1, 1, 2, 2]), 1)

    def test_tie_first_appearance_mid_list(self):
        self.assertEqual(mode([2, 3, 3, 2]), 2)

    def test_negative_numbers(self):
        self.assertEqual(mode([-3, -1, -1, -2]), -1)

    def test_floats(self):
        self.assertEqual(mode([1.5, 2.5, 1.5]), 1.5)

    def test_strings(self):
        self.assertEqual(mode(["a", "b", "a"]), "a")


if __name__ == "__main__":
    unittest.main()
