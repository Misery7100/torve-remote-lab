import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.duration import format_duration, parse_duration


class ParseDurationTest(unittest.TestCase):
    def test_single_unit_seconds(self):
        self.assertEqual(parse_duration("45s"), 45)

    def test_single_unit_minutes(self):
        self.assertEqual(parse_duration("90m"), 5400)

    def test_full_descending(self):
        self.assertEqual(parse_duration("1d2h3m4s"), 93784)

    def test_omitted_units(self):
        self.assertEqual(parse_duration("2h30m"), 9000)

    def test_non_normalized_input(self):
        self.assertEqual(parse_duration("24h"), 86400)

    def test_leading_negative(self):
        self.assertEqual(parse_duration("-1h30m"), -5400)

    def test_zero_value(self):
        self.assertEqual(parse_duration("0s"), 0)

    def test_units_out_of_order_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("1m1h")

    def test_units_out_of_order_far_apart_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("1s1d")

    def test_repeated_unit_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("2h2h")

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("")

    def test_unknown_unit_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("5x")

    def test_trailing_number_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("10")

    def test_trailing_only_negative_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("-")


class FormatDurationTest(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(format_duration(0), "0s")

    def test_seconds_only(self):
        self.assertEqual(format_duration(45), "45s")

    def test_largest_units_only(self):
        self.assertEqual(format_duration(90100), "1d1h1m40s")

    def test_zero_components_omitted(self):
        self.assertEqual(format_duration(7200), "2h")

    def test_leading_negative(self):
        self.assertEqual(format_duration(-9000), "-2h30m")


class RoundTripTest(unittest.TestCase):
    def test_round_trip_non_negative(self):
        for n in range(0, 1000000, 137):
            self.assertEqual(parse_duration(format_duration(n)), n)

    def test_round_trip_negative(self):
        for n in range(-1000000, 0, 97):
            self.assertEqual(parse_duration(format_duration(n)), n)

    def test_round_trip_edge_values(self):
        for n in [0, 1, 59, 60, 3600, 86400, -1, -86400]:
            self.assertEqual(parse_duration(format_duration(n)), n)


if __name__ == "__main__":
    unittest.main()
