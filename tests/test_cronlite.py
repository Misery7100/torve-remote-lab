import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.cronlite import next_run


class NextRunStepTest(unittest.TestCase):
    def test_step_from_zero(self):
        self.assertEqual(
            next_run("*/15", "*", (0, 0)), (0, 15)
        )

    def test_step_large_step_yields_zero_only(self):
        self.assertEqual(
            next_run("*/60", "*", (0, 0)), (1, 0)
        )

    def test_step_in_hour_spec(self):
        self.assertEqual(
            next_run("*", "*/6", (0, 5)), (0, 6)
        )


class NextRunRangeTest(unittest.TestCase):
    def test_minute_range(self):
        self.assertEqual(
            next_run("10-20", "*", (0, 9)), (0, 10)
        )

    def test_range_inclusive_bounds(self):
        self.assertEqual(
            next_run("10-20", "*", (0, 19)), (0, 20)
        )

    def test_hour_range(self):
        self.assertEqual(
            next_run("*", "9-17", (8, 59)), (9, 0)
        )


class NextRunCommaListTest(unittest.TestCase):
    def test_minute_comma_list(self):
        self.assertEqual(
            next_run("5,20,35", "*", (0, 4)), (0, 5)
        )

    def test_comma_list_second_value(self):
        self.assertEqual(
            next_run("5,20,35", "*", (0, 6)), (0, 20)
        )

    def test_hour_comma_list(self):
        self.assertEqual(
            next_run("*", "2,4,6", (1, 59)), (2, 0)
        )


class NextRunStrictlyAfterRuleTest(unittest.TestCase):
    def test_strictly_after_own_firing_time(self):
        self.assertEqual(
            next_run("30", "*", (4, 30)), (5, 30)
        )

    def test_next_given_after_is_firing(self):
        self.assertEqual(
            next_run("*/5", "*", (10, 15)), (10, 20)
        )


class NextRunRolloverTest(unittest.TestCase):
    def test_same_hour_rollover(self):
        self.assertEqual(
            next_run("0,30", "*", (3, 0)), (3, 30)
        )

    def test_next_hour_rollover(self):
        self.assertEqual(
            next_run("5", "*", (7, 6)), (8, 5)
        )

    def test_wrap_past_midnight(self):
        self.assertEqual(
            next_run("10", "*", (23, 59)), (0, 10)
        )

    def test_wrap_past_midnight_hour_based(self):
        self.assertEqual(
            next_run("*", "3", (23, 59)), (3, 0)
        )

    def test_end_of_day(self):
        self.assertEqual(
            next_run("30", "23", (23, 30)), (23, 30)
        )


class NextRunValidationTest(unittest.TestCase):
    def test_out_of_range_minute(self):
        with self.assertRaises(ValueError):
            next_run("60", "*", (0, 0))

    def test_out_of_range_hour(self):
        with self.assertRaises(ValueError):
            next_run("*", "24", (0, 0))

    def test_negative_minute(self):
        with self.assertRaises(ValueError):
            next_run("-1", "*", (0, 0))

    def test_negative_hour(self):
        with self.assertRaises(ValueError):
            next_run("*", "-2", (0, 0))

    def test_empty_minute_field(self):
        with self.assertRaises(ValueError):
            next_run("", "*", (0, 0))

    def test_empty_hour_field(self):
        with self.assertRaises(ValueError):
            next_run("*", "", (0, 0))

    def test_zero_step(self):
        with self.assertRaises(ValueError):
            next_run("*/0", "*", (0, 0))

    def test_negative_step(self):
        with self.assertRaises(ValueError):
            next_run("*/-3", "*", (0, 0))

    def test_malformed_step_no_slash_star(self):
        with self.assertRaises(ValueError):
            next_run("5/2", "*", (0, 0))

    def test_malformed_spec_alpha(self):
        with self.assertRaises(ValueError):
            next_run("foo", "*", (0, 0))

    def test_range_a_gt_b(self):
        with self.assertRaises(ValueError):
            next_run("20-10", "*", (0, 0))

    def test_out_of_range_in_comma_list(self):
        with self.assertRaises(ValueError):
            next_run("5,61,20", "*", (0, 0))

    def test_malformed_opening_dash_in_list(self):
        with self.assertRaises(ValueError):
            next_run("5,-3,20", "*", (0, 0))

    def test_leading_comma(self):
        with self.assertRaises(ValueError):
            next_run(",5,20", "*", (0, 0))

    def test_trailing_comma(self):
        with self.assertRaises(ValueError):
            next_run("5,20,", "*", (0, 0))


if __name__ == "__main__":
    unittest.main()
