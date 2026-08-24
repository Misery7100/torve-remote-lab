import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import roman_numeral


class RomanNumeralTest(unittest.TestCase):
    def test_ones(self):
        self.assertEqual(roman_numeral(1), "I")
        self.assertEqual(roman_numeral(2), "II")
        self.assertEqual(roman_numeral(3), "III")
        self.assertEqual(roman_numeral(4), "IV")

    def test_five_and_tens(self):
        self.assertEqual(roman_numeral(5), "V")
        self.assertEqual(roman_numeral(9), "IX")
        self.assertEqual(roman_numeral(10), "X")

    def test_twenties(self):
        self.assertEqual(roman_numeral(19), "XIX")
        self.assertEqual(roman_numeral(20), "XX")
        self.assertEqual(roman_numeral(29), "XXIX")

    def test_forty(self):
        self.assertEqual(roman_numeral(40), "XL")
        self.assertEqual(roman_numeral(49), "XLIX")

    def test_fifty(self):
        self.assertEqual(roman_numeral(50), "L")
        self.assertEqual(roman_numeral(99), "XCIX")

    def test_hundreds(self):
        self.assertEqual(roman_numeral(100), "C")
        self.assertEqual(roman_numeral(400), "CD")
        self.assertEqual(roman_numeral(499), "CDXCIX")

    def test_five_hundred(self):
        self.assertEqual(roman_numeral(500), "D")
        self.assertEqual(roman_numeral(999), "CMXCIX")

    def test_thousands(self):
        self.assertEqual(roman_numeral(1000), "M")
        self.assertEqual(roman_numeral(1994), "MCMXCIV")
        self.assertEqual(roman_numeral(2000), "MM")

    def test_upper_bound(self):
        self.assertEqual(roman_numeral(3999), "MMMCMXCIX")

    def test_below_range_raises(self):
        with self.assertRaises(ValueError):
            roman_numeral(0)
        with self.assertRaises(ValueError):
            roman_numeral(-1)

    def test_above_range_raises(self):
        with self.assertRaises(ValueError):
            roman_numeral(4000)
        with self.assertRaises(ValueError):
            roman_numeral(5000)

    def test_non_integer_raises(self):
        with self.assertRaises(ValueError):
            roman_numeral(3.5)


if __name__ == "__main__":
    unittest.main()
