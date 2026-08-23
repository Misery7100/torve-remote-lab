import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import char_count


class CharCountTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(char_count(""), 0)

    def test_whitespace_only(self):
        self.assertEqual(char_count("   \t  "), 0)

    def test_single_character(self):
        self.assertEqual(char_count("a"), 1)

    def test_single_word(self):
        self.assertEqual(char_count("hello"), 5)

    def test_multiple_words(self):
        self.assertEqual(char_count("hello world"), 10)

    def test_mixed_whitespace(self):
        self.assertEqual(char_count("one\t\ttwo\n three"), 11)

    def test_punctuation_counted(self):
        self.assertEqual(char_count("a, b. c!"), 6)

    def test_unicode_non_whitespace(self):
        self.assertEqual(char_count("héllø ☻"), 6)


if __name__ == "__main__":
    unittest.main()
