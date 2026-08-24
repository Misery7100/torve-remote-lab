import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import remove_punctuation


class RemovePunctuationTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(remove_punctuation(""), "")

    def test_no_punctuation(self):
        self.assertEqual(remove_punctuation("hello world"), "hello world")

    def test_all_punctuation(self):
        self.assertEqual(remove_punctuation("!?.,;:()[]{}\"'\\#"), "")

    def test_removes_punctuation_but_keeps_letters(self):
        self.assertEqual(remove_punctuation("Hello, world!"), "Hello world")

    def test_keeps_whitespace(self):
        self.assertEqual(remove_punctuation("a, b. c!"), "a b c")

    def test_keeps_digits(self):
        self.assertEqual(remove_punctuation("pi ~ 3.14159"), "pi  314159")

    def test_keeps_unicode(self):
        self.assertEqual(remove_punctuation("héllø, wörld!"), "héllø wörld")

    def test_removes_dollars_and_underscores(self):
        self.assertEqual(remove_punctuation("price $9  _under_score_"), "price 9  underscore")

    def test_all_ascii_punctuation_removed(self):
        import string

        self.assertEqual(remove_punctuation(string.punctuation), "")


if __name__ == "__main__":
    unittest.main()
