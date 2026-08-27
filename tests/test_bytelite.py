import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from math import fabs

from lab.bytelite import format_bytes, parse_bytes


class FormatBytesTest(unittest.TestCase):
    def test_plain_bytes_whole(self):
        self.assertEqual(format_bytes(0), "0 B")
        self.assertEqual(format_bytes(512), "512 B")
        self.assertEqual(format_bytes(1023), "1023 B")

    def test_kib_one_decimal(self):
        self.assertEqual(format_bytes(1024), "1.0 KiB")
        self.assertEqual(format_bytes(1536), "1.5 KiB")

    def test_mib_one_decimal(self):
        self.assertEqual(format_bytes(1024 ** 2), "1.0 MiB")
        self.assertEqual(format_bytes(2 * 1024 ** 2), "2.0 MiB")

    def test_gib_one_decimal(self):
        self.assertEqual(format_bytes(1024 ** 3), "1.0 GiB")

    def test_tib_one_decimal(self):
        self.assertEqual(format_bytes(1024 ** 4), "1.0 TiB")

    def test_value_uses_largest_unit(self):
        self.assertEqual(format_bytes(1024 ** 2 + 1024), "1.0 MiB")

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            format_bytes(-5)

    def test_non_integer_raises(self):
        with self.assertRaises(ValueError):
            format_bytes(1.5)


class ParseBytesTest(unittest.TestCase):
    def test_parse_whole_bytes(self):
        self.assertEqual(parse_bytes("512 B"), 512)
        self.assertEqual(parse_bytes("0 B"), 0)

    def test_parse_with_space(self):
        self.assertEqual(parse_bytes("1.5 KiB"), 1536)

    def test_parse_without_space(self):
        self.assertEqual(parse_bytes("512B"), 512)
        self.assertEqual(parse_bytes("1.5KiB"), 1536)

    def test_parse_case_insensitive(self):
        self.assertEqual(parse_bytes("2.0 MIB"), 2 * 1024 ** 2)
        self.assertEqual(parse_bytes("2.0mib"), 2 * 1024 ** 2)
        self.assertEqual(parse_bytes("2.0 MiB"), 2 * 1024 ** 2)

    def test_parse_gib(self):
        self.assertEqual(parse_bytes("1.0 GiB"), 1024 ** 3)

    def test_parse_tib(self):
        self.assertEqual(parse_bytes("1.5 TiB"), round(1.5 * 1024 ** 4))

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            parse_bytes("-1.5 KiB")

    def test_unknown_unit_raises(self):
        with self.assertRaises(ValueError):
            parse_bytes("5 x")

    def test_malformed_number_raises(self):
        for bad in ["1.5.5 KiB", ". KiB", "abc B", "1.2.3MiB", ""]:
            with self.assertRaises(ValueError):
                parse_bytes(bad)

    def test_bare_number_no_unit_raises(self):
        with self.assertRaises(ValueError):
            parse_bytes("512")


class RoundTripTest(unittest.TestCase):
    def assertRoundsBack(self, value):
        self.assertEqual(parse_bytes(format_bytes(value)), value)

    def test_round_trip_plain_bytes(self):
        for n in range(0, 1024, 7):
            self.assertRoundsBack(n)

    def test_round_trip_spread_of_counts(self):
        for n in [
            0,
            1,
            512,
            1023,
            1024,
            1536,
            1024 ** 2,
            int(2.5 * 1024 ** 2),
            1024 ** 3,
            1024 ** 4,
        ]:
            self.assertRoundsBack(n)

    UNIT_TOLERANCE = {
        "KiB": 0.06 * 1024,
        "MiB": 0.06 * 1024 ** 2,
        "GiB": 0.06 * 1024 ** 3,
        "TiB": 0.06 * 1024 ** 4,
    }

    def _formatted_unit(self, text):
        return text.split()[-1]

    def assertWithinRoundingTolerance(self, value):
        formatted = format_bytes(value)
        parsed = parse_bytes(formatted)
        unit = self._formatted_unit(formatted)
        tolerance = self.UNIT_TOLERANCE.get(unit, 0.0)
        self.assertLessEqual(
            fabs(parsed - value),
            tolerance,
            f"count {value} formatted {formatted!r} parsed to {parsed}",
        )

    def test_round_trip_within_tolerance(self):
        for n in range(1024, 5 * 1024 ** 4, 1000003):
            self.assertWithinRoundingTolerance(n)

    def test_round_trip_boundary_crossings(self):
        for n in [1023, 1024, 1025, 1024 ** 2 - 1, 1024 ** 2, 1024 ** 2 + 1]:
            self.assertWithinRoundingTolerance(n)


if __name__ == "__main__":
    unittest.main()
