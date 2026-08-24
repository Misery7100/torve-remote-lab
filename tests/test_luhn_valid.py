import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import luhn_valid


class LuhnValidTest(unittest.TestCase):
    def test_valid_card_number(self):
        self.assertTrue(luhn_valid("79927398713"))

    def test_invalid_card_number(self):
        self.assertFalse(luhn_valid("79927398710"))

    def test_single_valid_digit(self):
        self.assertTrue(luhn_valid("0"))

    def test_single_invalid_digit(self):
        self.assertFalse(luhn_valid("1"))

    def test_odd_length_number(self):
        self.assertTrue(luhn_valid("79927398713"))

    def test_even_length_number(self):
        self.assertTrue(luhn_valid("1234567812345670"))

    def test_spaces_raise_valueerror(self):
        with self.assertRaises(ValueError):
            luhn_valid("7992 7398 713")

    def test_non_digit_raises_valueerror(self):
        with self.assertRaises(ValueError):
            luhn_valid("abc")

    def test_mixed_characters_raise_valueerror(self):
        with self.assertRaises(ValueError):
            luhn_valid("7992abc713")

    def test_punctuation_raises_valueerror(self):
        with self.assertRaises(ValueError):
            luhn_valid("7992-7398")

    def test_empty_string_passes(self):
        self.assertTrue(luhn_valid(""))


if __name__ == "__main__":
    unittest.main()
