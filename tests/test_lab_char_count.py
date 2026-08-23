import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import char_count


class CharCountTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(char_count(""), 0)

    def test_whitespace_only(self):
        self.assertEqual(char_count("   \t  \n"), 0)

    def test_single_word(self):
        self.assertEqual(char_count("hello"), 5)

    def test_multiple_words(self):
        self.assertEqual(char_count("hello world"), 10)

    def test_repeated_whitespace(self):
        self.assertEqual(char_count("  one   two  three  "), 11)

    def test_tabs_and_newlines(self):
        self.assertEqual(char_count("a\tb\nc d"), 4)

    def test_punctuation(self):
        self.assertEqual(char_count("hi, world!"), 9)


if __name__ == "__main__":
    unittest.main()
