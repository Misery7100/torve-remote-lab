import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import count_words, reverse_words


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


class ReverseWordsTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(reverse_words(""), "")

    def test_whitespace_only(self):
        self.assertEqual(reverse_words("   \t  "), "")

    def test_single_word(self):
        self.assertEqual(reverse_words("hello"), "hello")

    def test_multiple_words(self):
        self.assertEqual(reverse_words("hello world"), "world hello")

    def test_repeated_whitespace(self):
        self.assertEqual(reverse_words("  one   two  three  "), "three two one")

    def test_three_words(self):
        self.assertEqual(reverse_words("the quick brown fox"), "fox brown quick the")


if __name__ == "__main__":
    unittest.main()
