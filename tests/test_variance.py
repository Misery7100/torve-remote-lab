import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.stats import variance


class VarianceSampleTest(unittest.TestCase):
    def test_known_sample(self):
        self.assertEqual(variance([1, 2, 3, 4, 5]), 2.5)

    def test_two_elements(self):
        self.assertEqual(variance([2, 4]), 2)

    def test_identical_values(self):
        self.assertEqual(variance([3, 3, 3, 3]), 0)

    def test_float_result(self):
        self.assertAlmostEqual(variance([1, 2, 4, 8, 16]), 37.2)

    def test_single_element_raises_valueerror(self):
        with self.assertRaises(ValueError):
            variance([5])

    def test_empty_raises_valueerror(self):
        with self.assertRaises(ValueError):
            variance([])

    def test_default_is_sample(self):
        self.assertNotEqual(variance([1, 2, 3, 4, 5]), variance([1, 2, 3, 4, 5], sample=False))


class VariancePopulationTest(unittest.TestCase):
    def test_known_population(self):
        self.assertEqual(variance([1, 2, 3, 4, 5], sample=False), 2)

    def test_two_elements(self):
        self.assertEqual(variance([2, 4], sample=False), 1)

    def test_single_element_returns_zero(self):
        self.assertEqual(variance([5], sample=False), 0)

    def test_empty_raises_valueerror(self):
        with self.assertRaises(ValueError):
            variance([], sample=False)


class VarianceImmutabilityTest(unittest.TestCase):
    def test_input_not_mutated(self):
        numbers = [3, 1, 4, 1, 5, 9, 2, 6]
        original = list(numbers)
        variance(numbers)
        variance(numbers, sample=False)
        self.assertEqual(numbers, original)

    def test_returns_float(self):
        self.assertIsInstance(variance([2, 4]), float)
        self.assertIsInstance(variance([2, 4], sample=False), float)


if __name__ == "__main__":
    unittest.main()
