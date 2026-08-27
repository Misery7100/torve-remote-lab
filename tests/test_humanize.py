import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.humanize import format_bytes, format_seconds


class FormatBytesTest(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(format_bytes(0), "0 B")

    def test_whole_bytes(self):
        self.assertEqual(format_bytes(512), "512 B")

    def test_single_byte(self):
        self.assertEqual(format_bytes(1), "1 B")

    def test_boundary_one_kib(self):
        self.assertEqual(format_bytes(1024), "1 KiB")

    def test_fractional_kib(self):
        self.assertEqual(format_bytes(1536), "1.5 KiB")

    def test_exact_mib_drops_zero_decimal(self):
        self.assertEqual(format_bytes(2048), "2 KiB")

    def test_fractional_mib(self):
        self.assertEqual(format_bytes(3145728), "3 MiB")

    def test_higher_units(self):
        self.assertEqual(format_bytes(1024 ** 4), "1 TiB")

    def test_large_value(self):
        self.assertEqual(format_bytes(int(5.5 * 1024 ** 3)), "5.5 GiB")

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            format_bytes(-1)

    def test_non_integer_raises(self):
        with self.assertRaises(ValueError):
            format_bytes(1.5)

    def test_non_numeric_raises(self):
        with self.assertRaises(ValueError):
            format_bytes("512")


class FormatSecondsTest(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(format_seconds(0), "0s")

    def test_seconds_only(self):
        self.assertEqual(format_seconds(5), "5s")

    def test_minutes_only(self):
        self.assertEqual(format_seconds(120), "2m")

    def test_hours_only(self):
        self.assertEqual(format_seconds(7200), "2h")

    def test_mixed_full(self):
        self.assertEqual(format_seconds(3661), "1h 1m 1s")

    def test_mid_components_omitted(self):
        self.assertEqual(format_seconds(3660), "1h 1m")

    def test_minutes_omitted(self):
        self.assertEqual(format_seconds(3601), "1h 1s")

    def test_seconds_omitted(self):
        self.assertEqual(format_seconds(3600), "1h")

    def test_hour_minute_second(self):
        self.assertEqual(format_seconds(3901), "1h 5m 1s")

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            format_seconds(-1)

    def test_non_integer_raises(self):
        with self.assertRaises(ValueError):
            format_seconds(1.5)

    def test_non_numeric_raises(self):
        with self.assertRaises(ValueError):
            format_seconds("60")


if __name__ == "__main__":
    unittest.main()
