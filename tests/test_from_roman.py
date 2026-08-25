import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import from_roman, roman_numeral


class FromRomanTest(unittest.TestCase):
    def test_ones(self):
        self.assertEqual(from_roman("I"), 1)
        self.assertEqual(from_roman("II"), 2)
        self.assertEqual(from_roman("III"), 3)
        self.assertEqual(from_roman("IV"), 4)

    def test_five_and_tens(self):
        self.assertEqual(from_roman("V"), 5)
        self.assertEqual(from_roman("IX"), 9)
        self.assertEqual(from_roman("X"), 10)

    def test_twenties(self):
        self.assertEqual(from_roman("XIX"), 19)
        self.assertEqual(from_roman("XX"), 20)
        self.assertEqual(from_roman("XXIX"), 29)

    def test_forty(self):
        self.assertEqual(from_roman("XL"), 40)
        self.assertEqual(from_roman("XLIX"), 49)

    def test_fifty(self):
        self.assertEqual(from_roman("L"), 50)
        self.assertEqual(from_roman("XCIX"), 99)

    def test_hundreds(self):
        self.assertEqual(from_roman("C"), 100)
        self.assertEqual(from_roman("CD"), 400)
        self.assertEqual(from_roman("CDXCIX"), 499)

    def test_five_hundred(self):
        self.assertEqual(from_roman("D"), 500)
        self.assertEqual(from_roman("CMXCIX"), 999)

    def test_thousands(self):
        self.assertEqual(from_roman("M"), 1000)
        self.assertEqual(from_roman("MCMXCIV"), 1994)
        self.assertEqual(from_roman("MM"), 2000)

    def test_upper_bound(self):
        self.assertEqual(from_roman("MMMCMXCIX"), 3999)

    def test_invalid_char_raises(self):
        with self.assertRaises(ValueError):
            from_roman("IIII")
        with self.assertRaises(ValueError):
            from_roman("VX")
        with self.assertRaises(ValueError):
            from_roman("")
        with self.assertRaises(ValueError):
            from_roman("hello")

    def test_non_string_raises(self):
        with self.assertRaises(ValueError):
            from_roman(123)
        with self.assertRaises(ValueError):
            from_roman(None)


class FromRomanRoundTripTest(unittest.TestCase):
    def test_round_trip(self):
        for n in range(1, 4000):
            self.assertEqual(from_roman(roman_numeral(n)), n)


if __name__ == "__main__":
    unittest.main()
