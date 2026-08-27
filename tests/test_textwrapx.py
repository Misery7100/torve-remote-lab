import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.textwrapx import justify, wrap


class WrapTest(unittest.TestCase):
    def test_single_line(self):
        self.assertEqual(wrap("ab cd", 5), ["ab cd"])

    def test_multiple_lines(self):
        self.assertEqual(wrap("aaa bbb ccc ddd", 3), ["aaa", "bbb", "ccc", "ddd"])

    def test_long_word_hard_broken(self):
        self.assertEqual(wrap("abcdefgh", 3), ["abc", "def", "gh"])

    def test_long_word_exact_multiple(self):
        self.assertEqual(wrap("abcdefghij", 5), ["abcde", "fghij"])

    def test_long_word_then_short(self):
        self.assertEqual(wrap("aa bbbbbbbbbbb cc", 5), ["aa", "bbbbb", "bbbbb", "b cc"])

    def test_no_line_exceeds_width(self):
        for line in wrap("the quick brown fox jumps over the lazy dog", 12):
            self.assertLessEqual(len(line), 12)

    def test_empty_text(self):
        self.assertEqual(wrap("", 5), [])

    def test_width_zero_raises(self):
        with self.assertRaises(ValueError):
            wrap("hello", 0)

    def test_negative_width_raises(self):
        with self.assertRaises(ValueError):
            wrap("hello", -1)


class JustifyTest(unittest.TestCase):
    def test_returns_single_line(self):
        self.assertEqual(justify("ab cd", 5), ["ab cd"])

    def test_equal_width_lines(self):
        result = justify("the quick brown fox jumps over the lazy dog", 12)
        self.assertEqual(len(result), len(wrap("the quick brown fox jumps over the lazy dog", 12)))
        for line in result[:-1]:
            self.assertEqual(len(line), 12)

    def test_last_line_left_aligned(self):
        text = "the quick brown fox jumps over the lazy dog"
        result = justify(text, 12)
        self.assertEqual(result[-1], wrap(text, 12)[-1])

    def test_single_word_line_unchanged(self):
        text = "supercalifragilisticexpialidocious tiny"
        result = justify(text, 5)
        self.assertEqual(result[0], "super")

    def test_left_biased_distribution(self):
        text = "aa bbb cc dddd e"
        result = justify(text, 8)
        self.assertEqual(len(result[0]), 8)
        self.assertEqual(result[0].split(), ["aa", "bbb"])
        self.assertNotEqual(result[0], "aa bbb cc")

    def test_each_justified_line_len_width(self):
        text = "one two three four five six seven eight nine ten"
        for line in justify(text, 15)[:-1]:
            self.assertEqual(len(line), 15)

    def test_width_zero_raises(self):
        with self.assertRaises(ValueError):
            justify("hello", 0)

    def test_negative_width_raises(self):
        with self.assertRaises(ValueError):
            justify("hello", -1)


if __name__ == "__main__":
    unittest.main()
