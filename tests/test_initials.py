import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import initials


class InitialsTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(initials(""), "")

    def test_whitespace_only(self):
        self.assertEqual(initials("   \t  "), "")

    def test_single_word(self):
        self.assertEqual(initials("hello"), "H")

    def test_lowercases_uppercased(self):
        self.assertEqual(initials("hello"), "H")
        self.assertEqual(initials("Robert"), "R")

    def test_multiple_words_joined(self):
        self.assertEqual(initials("National Aeronautics Space Administration"), "NASA")

    def test_two_words(self):
        self.assertEqual(initials("John Smith"), "JS")

    def test_takes_first_letter_of_each_word(self):
        self.assertEqual(initials("the quick brown fox"), "TQBF")

    def test_repeated_whitespace(self):
        self.assertEqual(initials("  one   two  three  "), "OTT")

    def test_tabs_and_newlines(self):
        self.assertEqual(initials("hello\t\tworld\n"), "HW")


if __name__ == "__main__":
    unittest.main()
