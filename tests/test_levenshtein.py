import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import levenshtein


class LevenshteinTest(unittest.TestCase):
    def test_empty_both(self):
        self.assertEqual(levenshtein("", ""), 0)

    def test_empty_left(self):
        self.assertEqual(levenshtein("", "abc"), 3)

    def test_empty_right(self):
        self.assertEqual(levenshtein("abc", ""), 3)

    def test_identical(self):
        self.assertEqual(levenshtein("kitten", "kitten"), 0)

    def test_known_kitten_sitting(self):
        self.assertEqual(levenshtein("kitten", "sitting"), 3)

    def test_single_character(self):
        self.assertEqual(levenshtein("a", "a"), 0)
        self.assertEqual(levenshtein("a", "b"), 1)

    def test_substitution(self):
        self.assertEqual(levenshtein("abc", "abd"), 1)

    def test_insertion(self):
        self.assertEqual(levenshtein("abc", "abcd"), 1)

    def test_deletion(self):
        self.assertEqual(levenshtein("abcd", "abc"), 1)

    def test_transposition_costs_two(self):
        self.assertEqual(levenshtein("ab", "ba"), 2)

    def test_adjacent_transposition(self):
        self.assertEqual(levenshtein("kitten", "ikitten"), 1)
        self.assertEqual(levenshtein("abcd", "acbd"), 2)

    def test_symmetry(self):
        self.assertEqual(levenshtein("saturday", "sunday"), 3)
        self.assertEqual(levenshtein("sunday", "saturday"), 3)

    def test_unicode(self):
        self.assertEqual(levenshtein("caf\u00e9", "caf\u00e9"), 0)
        self.assertEqual(levenshtein("caf\u00e9", "cafe"), 1)
        self.assertEqual(levenshtein("\u4f60\u597d", "\u4f50\u597d"), 1)
        self.assertEqual(levenshtein("\u4f60\u597d", "\u4f60\u597d\u4e16\u754c"), 2)

    def test_unrelated_strings(self):
        self.assertEqual(levenshtein("abc", "xyz"), 3)


if __name__ == "__main__":
    unittest.main()
