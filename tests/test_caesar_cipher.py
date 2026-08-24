import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import caesar_cipher


class CaesarCipherTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(caesar_cipher("", 3), "")

    def test_lowercase_rotate_forward(self):
        self.assertEqual(caesar_cipher("abc", 3), "def")

    def test_lowercase_wraps_around(self):
        self.assertEqual(caesar_cipher("xyz", 3), "abc")

    def test_uppercase_rotate_forward(self):
        self.assertEqual(caesar_cipher("ABC", 3), "DEF")

    def test_uppercase_wraps_around(self):
        self.assertEqual(caesar_cipher("XYZ", 3), "ABC")

    def test_preserves_case(self):
        self.assertEqual(caesar_cipher("AbC", 2), "CdE")

    def test_leaves_non_letters_untouched(self):
        self.assertEqual(caesar_cipher("abc 123 !@#", 1), "bcd 123 !@#")

    def test_negative_shift(self):
        self.assertEqual(caesar_cipher("abc", -3), "xyz")

    def test_negative_shift_uppercase_wraps(self):
        self.assertEqual(caesar_cipher("ABC", -3), "XYZ")

    def test_zero_shift(self):
        self.assertEqual(caesar_cipher("hello", 0), "hello")

    def test_shift_larger_than_26(self):
        self.assertEqual(caesar_cipher("abc", 29), "def")

    def test_shift_of_26_no_change(self):
        self.assertEqual(caesar_cipher("hello", 26), "hello")


if __name__ == "__main__":
    unittest.main()
