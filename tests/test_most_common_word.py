import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import most_common_word


class MostCommonWordTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(most_common_word(""), "")

    def test_whitespace_only(self):
        self.assertEqual(most_common_word("   \t  "), "")

    def test_single_word(self):
        self.assertEqual(most_common_word("hello"), "hello")

    def test_single_word_upper(self):
        self.assertEqual(most_common_word("HELLO"), "hello")

    def test_distinct_words(self):
        self.assertEqual(most_common_word("a b c"), "a")

    def test_mixed_case_identity(self):
        self.assertEqual(most_common_word("Hello hello HELLO"), "hello")

    def test_common_word(self):
        self.assertEqual(most_common_word("the quick the brown the fox"), "the")

    def test_breaks_ties_by_first_appearance(self):
        self.assertEqual(most_common_word("apple banana apple cherry banana"), "apple")

    def test_repeated_whitespace(self):
        self.assertEqual(most_common_word("  one   two  one  "), "one")

    def test_tabs_and_newlines(self):
        self.assertEqual(most_common_word("one\ttwo\none"), "one")


if __name__ == "__main__":
    unittest.main()
