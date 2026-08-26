import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.isodate import day_of_year, iso_week


class IsoWeekBoundariesTest(unittest.TestCase):
    def test_2016_01_01_is_iso_2015_w53_d5(self):
        self.assertEqual(iso_week(2016, 1, 1), (2015, 53, 5))

    def test_2021_01_01_is_iso_2020_w53_d5(self):
        self.assertEqual(iso_week(2021, 1, 1), (2020, 53, 5))

    def test_2018_12_31_is_iso_2019_w01_d1(self):
        self.assertEqual(iso_week(2018, 12, 31), (2019, 1, 1))

    def test_2021_01_04_is_iso_2021_w01_d1(self):
        self.assertEqual(iso_week(2021, 1, 4), (2021, 1, 1))


class IsoWeekCalendarTest(unittest.TestCase):
    def test_monday_is_first_weekday(self):
        self.assertEqual(iso_week(2021, 5, 31)[2], 1)
        self.assertEqual(iso_week(2021, 5, 30)[2], 7)

    def test_2020_leap_has_53_iso_weeks(self):
        self.assertEqual(iso_week(2020, 1, 1), (2020, 1, 3))
        self.assertEqual(iso_week(2020, 12, 27)[1], 52)
        self.assertEqual(iso_week(2020, 12, 28), (2020, 53, 1))
        self.assertEqual(iso_week(2021, 1, 3), (2020, 53, 7))


class LeapCenturyTest(unittest.TestCase):
    def test_1900_not_leap(self):
        self.assertEqual(day_of_year(1900, 2, 28), 59)
        with self.assertRaises(ValueError):
            iso_week(1900, 2, 29)

    def test_2000_is_leap(self):
        self.assertEqual(day_of_year(2000, 2, 29), 60)
        self.assertEqual(day_of_year(2000, 12, 31), 366)


class DayOfYearTest(unittest.TestCase):
    def test_january_first(self):
        self.assertEqual(day_of_year(2021, 1, 1), 1)

    def test_december_31_common_year(self):
        self.assertEqual(day_of_year(2021, 12, 31), 365)

    def test_leap_year_february(self):
        self.assertEqual(day_of_year(2024, 2, 29), 60)
        self.assertEqual(day_of_year(2024, 12, 31), 366)


class ValidationTest(unittest.TestCase):
    def test_invalid_month(self):
        with self.assertRaises(ValueError):
            iso_week(2021, 13, 1)
        with self.assertRaises(ValueError):
            day_of_year(2021, 0, 1)

    def test_invalid_day_in_common_february(self):
        with self.assertRaises(ValueError):
            iso_week(2021, 2, 29)
        with self.assertRaises(ValueError):
            day_of_year(2021, 2, 30)

    def test_invalid_day_for_month(self):
        with self.assertRaises(ValueError):
            iso_week(2021, 4, 31)
        with self.assertRaises(ValueError):
            day_of_year(2021, 6, 31)

    def test_invalid_day_zero(self):
        with self.assertRaises(ValueError):
            iso_week(2021, 3, 0)


class DatetimeOracleSweepTest(unittest.TestCase):
    def test_iso_week_matches_datetime_oracle(self):
        start = date(1995, 1, 1)
        end = date(2025, 12, 31)
        current = start
        checked = 0
        while current <= end:
            iso_year, iso_week_number, iso_weekday = iso_week(
                current.year, current.month, current.day
            )
            self.assertEqual(
                (iso_year, iso_week_number, iso_weekday),
                current.isocalendar(),
                msg=str(current),
            )
            current += timedelta(days=1)
            checked += 1
        self.assertGreater(checked, 11000)


class DayOfYearOracleSweepTest(unittest.TestCase):
    def test_day_of_year_matches_datetime_oracle(self):
        start = date(1995, 1, 1)
        end = date(2025, 12, 31)
        current = start
        checked = 0
        while current <= end:
            self.assertEqual(
                day_of_year(current.year, current.month, current.day),
                current.timetuple().tm_yday,
                msg=str(current),
            )
            current += timedelta(days=1)
            checked += 1
        self.assertGreater(checked, 11000)


if __name__ == "__main__":
    unittest.main()
