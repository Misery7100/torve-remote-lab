import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.textutil import titlecase


class TitlecaseTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(titlecase(""), "")

    def test_single_word(self):
        self.assertEqual(titlecase("hello"), "Hello")

    def test_multiple_words(self):
        self.assertEqual(titlecase("hello world"), "Hello World")

    def test_already_capitalized(self):
        self.assertEqual(titlecase("Hello World"), "Hello World")

    def test_mixed_case(self):
        self.assertEqual(titlecase("tHe qUiCk bRoWn"), "The Quick Brown")


if __name__ == "__main__":
    unittest.main()
