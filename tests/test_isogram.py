import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import is_isogram


class IsIsogramTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertTrue(is_isogram(""))

    def test_single_letter(self):
        self.assertTrue(is_isogram("a"))

    def test_all_unique_letters(self):
        self.assertTrue(is_isogram("isogram"))

    def test_no_repeated_letters(self):
        self.assertTrue(is_isogram("uncopyrightable"))

    def test_repeated_letter(self):
        self.assertFalse(is_isogram("hello"))

    def test_ignores_case(self):
        self.assertFalse(is_isogram("Alphabet"))
        self.assertFalse(is_isogram("Deeply"))

    def test_ignores_repeated_case_insensitively(self):
        self.assertFalse(is_isogram("BaRBara"))

    def test_ignores_non_letter_characters(self):
        self.assertTrue(is_isogram("six-year-old"))
        self.assertFalse(is_isogram("The Big Bang"))

    def test_only_non_letters(self):
        self.assertTrue(is_isogram("123 !?.,;:"))

    def test_repeated_after_ignored_characters(self):
        self.assertFalse(is_isogram("a-b-a"))

    def test_whitespace_ignored(self):
        self.assertTrue(is_isogram("A B C"))
        self.assertFalse(is_isogram("A B A"))


if __name__ == "__main__":
    unittest.main()
