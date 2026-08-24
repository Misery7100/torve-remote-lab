import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import is_isogram


class IsIsogramTest(unittest.TestCase):
    def test_simple_isogram(self):
        self.assertTrue(is_isogram("isogram"))

    def test_ignores_case(self):
        self.assertTrue(is_isogram("Subdermatoglyphic"))
        self.assertTrue(is_isogram("AbCd"))

    def test_repeated_letter(self):
        self.assertFalse(is_isogram("hello"))

    def test_repeated_letter_different_case(self):
        self.assertFalse(is_isogram("AbA"))
        self.assertFalse(is_isogram("Antimony"))

    def test_ignores_non_letters(self):
        self.assertTrue(is_isogram("six-year-old"))
        self.assertTrue(is_isogram("abc 123 !?"))

    def test_repeats_separated_by_non_letters_still_count(self):
        self.assertFalse(is_isogram("ab-cd A"))

    def test_empty_string(self):
        self.assertTrue(is_isogram(""))

    def test_only_non_letters(self):
        self.assertTrue(is_isogram("1234  !? ..."))

    def test_single_character(self):
        self.assertTrue(is_isogram("a"))


if __name__ == "__main__":
    unittest.main()
