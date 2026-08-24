import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import hamming_distance


class HammingDistanceTest(unittest.TestCase):
    def test_identical_strings(self):
        self.assertEqual(hamming_distance("hello", "hello"), 0)

    def test_single_differs(self):
        self.assertEqual(hamming_distance("karolin", "kathrin"), 3)

    def test_all_differ(self):
        self.assertEqual(hamming_distance("abc", "xyz"), 3)

    def test_single_character(self):
        self.assertEqual(hamming_distance("a", "a"), 0)
        self.assertEqual(hamming_distance("a", "b"), 1)

    def test_empty_strings(self):
        self.assertEqual(hamming_distance("", ""), 0)

    def test_differing_case(self):
        self.assertEqual(hamming_distance("Hello", "hello"), 1)

    def test_symmetry(self):
        self.assertEqual(hamming_distance("abcd", "abce"), 1)
        self.assertEqual(hamming_distance("abce", "abcd"), 1)

    def test_unequal_lengths_raises(self):
        with self.assertRaises(ValueError):
            hamming_distance("abc", "ab")

    def test_unequal_lengths_one_empty_raises(self):
        with self.assertRaises(ValueError):
            hamming_distance("abc", "")


if __name__ == "__main__":
    unittest.main()
