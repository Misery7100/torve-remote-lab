import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import wrap_text


class WrapTextExactFitTest(unittest.TestCase):
    def test_single_exact_fit_line(self):
        self.assertEqual(wrap_text("ab cd", 5), ["ab cd"])

    def test_multiple_exact_fit_lines(self):
        self.assertEqual(wrap_text("aaa bbb ccc ddd", 3), ["aaa", "bbb", "ccc", "ddd"])

    def test_many_shorter_words_exceed_width(self):
        self.assertEqual(wrap_text("0 1 2 3 4 5", 5), ["0 1 2", "3 4 5"])


class WrapTextLongWordTest(unittest.TestCase):
    def test_single_long_word_split_into_chunks(self):
        self.assertEqual(wrap_text("abcdefgh", 3), ["abc", "def", "gh"])

    def test_long_word_split_exact_multiple(self):
        self.assertEqual(wrap_text("abcdefghij", 5), ["abcde", "fghij"])

    def test_word_after_long_word(self):
        self.assertEqual(wrap_text("aa bbbbbbbbbbb cc", 5), ["aa", "bbbbb", "bbbbb", "b cc"])


class WrapTextSpaceCollapseTest(unittest.TestCase):
    def test_runs_of_spaces_collapse_to_one(self):
        self.assertEqual(wrap_text("a   b   c", 5), ["a b c"])

    def test_leading_and_trailing_spaces_stripped(self):
        self.assertEqual(wrap_text("   aa bb   ", 5), ["aa bb"])


class WrapTextNewlineAndTabTest(unittest.TestCase):
    def test_newline_inside_word_is_preserved_not_collapsed(self):
        self.assertEqual(wrap_text("a\n\nb", 5), ["a\n\nb"])

    def test_tabs_inside_word_are_preserved_not_collapsed(self):
        self.assertEqual(wrap_text("a\t\tb", 5), ["a\t\tb"])


class WrapTextEmptyTest(unittest.TestCase):
    def test_empty_text(self):
        self.assertEqual(wrap_text("", 5), [])

    def test_all_space_text(self):
        self.assertEqual(wrap_text("     ", 5), [])


class WrapTextWidthValidationTest(unittest.TestCase):
    def test_width_zero_raises(self):
        with self.assertRaises(ValueError):
            wrap_text("hello", 0)

    def test_negative_width_raises(self):
        with self.assertRaises(ValueError):
            wrap_text("hello", -1)


if __name__ == "__main__":
    unittest.main()
