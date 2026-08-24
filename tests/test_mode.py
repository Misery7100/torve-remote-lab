import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.stats import mode


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
