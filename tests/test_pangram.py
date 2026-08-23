import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import is_pangram


class IsPangramTest(unittest.TestCase):
    def test_perfect_pangram(self):
        self.assertTrue(is_pangram("the quick brown fox jumps over the lazy dog"))

    def test_ignores_case(self):
        self.assertTrue(is_pangram("The Quick Brown Fox Jumps Over The Lazy Dog"))

    def test_ignores_punctuation_and_whitespace(self):
        self.assertTrue(
            is_pangram("The five boxing wizards jump quickly. (Really!)")
        )

    def test_non_pangram(self):
        self.assertFalse(is_pangram("hello world"))

    def test_empty_string(self):
        self.assertFalse(is_pangram(""))

    def test_only_whitespace(self):
        self.assertFalse(is_pangram("   \t  "))

    def test_repeated_letters_still_full_alphabet(self):
        self.assertTrue(is_pangram("aabcdefghijklmnopqrstuvwxyz"))

    def test_missing_single_letter(self):
        self.assertFalse(
            is_pangram("the quick brown fox jumps over the laz dog")
        )


if __name__ == "__main__":
    unittest.main()
