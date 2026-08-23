import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import count_words, is_palindrome


class CountWordsTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(count_words(""), 0)

    def test_whitespace_only(self):
        self.assertEqual(count_words("   \t  "), 0)

    def test_single_word(self):
        self.assertEqual(count_words("hello"), 1)

    def test_multiple_words(self):
        self.assertEqual(count_words("hello world"), 2)

    def test_repeated_whitespace(self):
        self.assertEqual(count_words("  one   two  three  "), 3)

    def test_words_separated_by_tabs_and_newlines(self):
        self.assertEqual(count_words("one\t\ttwo\n three"), 3)


class IsPalindromeTest(unittest.TestCase):
    def test_simple_palindrome(self):
        self.assertTrue(is_palindrome("racecar"))

    def test_case_insensitive(self):
        self.assertTrue(is_palindrome("RaceCar"))

    def test_ignores_spaces(self):
        self.assertTrue(is_palindrome("a man a plan a canal panama"))

    def test_non_palindrome(self):
        self.assertFalse(is_palindrome("hello"))

    def test_single_character(self):
        self.assertTrue(is_palindrome("a"))

    def test_empty_string(self):
        self.assertTrue(is_palindrome(""))

    def test_non_palindrome_with_spaces(self):
        self.assertFalse(is_palindrome("not a palindrome test"))


if __name__ == "__main__":
    unittest.main()
