import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.casing import snake_case


class SnakeCaseTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(snake_case(""), "")

    def test_single_word(self):
        self.assertEqual(snake_case("hello"), "hello")

    def test_single_uppercase_word(self):
        self.assertEqual(snake_case("HELLO"), "hello")

    def test_multiple_words(self):
        self.assertEqual(snake_case("hello world"), "hello_world")

    def test_mixed_case(self):
        self.assertEqual(snake_case("Hello World"), "hello_world")

    def test_three_words(self):
        self.assertEqual(snake_case("the quick brown fox"), "the_quick_brown_fox")

    def test_repeated_whitespace(self):
        self.assertEqual(snake_case("  one   two  three  "), "one_two_three")


if __name__ == "__main__":
    unittest.main()
