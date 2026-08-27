import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.checksum import compute_damm_check_digit, damm_valid, luhn_valid


class LuhnValidTest(unittest.TestCase):
    def test_valid_card_number(self):
        self.assertTrue(luhn_valid("79927398713"))

    def test_invalid_card_number(self):
        self.assertFalse(luhn_valid("79927398710"))

    def test_single_valid_digit(self):
        self.assertTrue(luhn_valid("0"))

    def test_single_invalid_digit(self):
        self.assertFalse(luhn_valid("1"))

    def test_even_length_number(self):
        self.assertTrue(luhn_valid("1234567812345670"))

    def test_invalid_even_length_number(self):
        self.assertFalse(luhn_valid("1234567812345671"))

    def test_empty_string_passes(self):
        self.assertTrue(luhn_valid(""))

    def test_non_digit_raises_valueerror(self):
        with self.assertRaises(ValueError):
            luhn_valid("abc")

    def test_spaces_raise_valueerror(self):
        with self.assertRaises(ValueError):
            luhn_valid("7992 7398 713")

    def test_mixed_characters_raise_valueerror(self):
        with self.assertRaises(ValueError):
            luhn_valid("7992abc713")

    def test_longer_valid_number(self):
        self.assertTrue(luhn_valid("49927398716"))


class DammCheckDigitTest(unittest.TestCase):
    def test_single_digit_source(self):
        self.assertEqual(compute_damm_check_digit("5"), "9")

    def test_known_check_digit(self):
        self.assertEqual(compute_damm_check_digit("572"), "4")

    def test_computed_digit_validates(self):
        for digits in ("572", "123", "79927398713", "0", "9"):
            full = digits + compute_damm_check_digit(digits)
            self.assertTrue(damm_valid(full))

    def test_empty_string(self):
        self.assertEqual(compute_damm_check_digit(""), "0")

    def test_non_digit_raises_valueerror(self):
        with self.assertRaises(ValueError):
            compute_damm_check_digit("57a")


class DammValidTest(unittest.TestCase):
    def test_valid_full_string(self):
        self.assertTrue(damm_valid("5724"))

    def test_invalid_full_string(self):
        self.assertFalse(damm_valid("5725"))
        self.assertFalse(damm_valid("5723"))

    def test_a_single_corrupted_digit_is_caught(self):
        self.assertFalse(damm_valid("79927398713" + "0"))

    def test_valid_full_string_from_check_digit(self):
        self.assertTrue(damm_valid("79927398713" + compute_damm_check_digit("79927398713")))

    def test_non_digit_raises_valueerror(self):
        with self.assertRaises(ValueError):
            damm_valid("57a4")

    def test_spaces_raise_valueerror(self):
        with self.assertRaises(ValueError):
            damm_valid("572 4")


if __name__ == "__main__":
    unittest.main()
