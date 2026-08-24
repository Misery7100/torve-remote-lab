import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import balanced_brackets


class BalancedBracketsTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertTrue(balanced_brackets(""))

    def test_simple_pairs(self):
        self.assertTrue(balanced_brackets("()[]{}"))

    def test_nested_pairs(self):
        self.assertTrue(balanced_brackets("([{}])"))

    def test_balanced_with_other_characters(self):
        self.assertTrue(balanced_brackets("(a[b]{c})d(e)"))

    def test_ignores_non_bracket_characters(self):
        self.assertTrue(balanced_brackets("hello world 123 !@#"))

    def test_mismatched_close(self):
        self.assertFalse(balanced_brackets("(]"))

    def test_mismatched_order(self):
        self.assertFalse(balanced_brackets("([)]"))

    def test_unclosed_open(self):
        self.assertFalse(balanced_brackets("(()"))

    def test_unopened_close(self):
        self.assertFalse(balanced_brackets(")("))

    def test_wrong_bracket_close(self):
        self.assertFalse(balanced_brackets("{()]"))


if __name__ == "__main__":
    unittest.main()
