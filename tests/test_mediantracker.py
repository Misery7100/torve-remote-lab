import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.mediantracker import MedianTracker


class MedianTrackerTest(unittest.TestCase):
    def test_empty_tracker_median_raises_valueerror(self):
        with self.assertRaises(ValueError):
            MedianTracker().median()

    def test_single_value_odd_count(self):
        tracker = MedianTracker()
        tracker.add(5)
        self.assertEqual(tracker.median(), 5)

    def test_three_values_odd_count(self):
        tracker = MedianTracker()
        for value in (3, 1, 2):
            tracker.add(value)
        self.assertEqual(tracker.median(), 2)

    def test_four_values_even_count_returns_mean(self):
        tracker = MedianTracker()
        for value in (1, 2, 3, 4):
            tracker.add(value)
        self.assertEqual(tracker.median(), 2.5)

    def test_two_values_even_count_returns_mean(self):
        tracker = MedianTracker()
        tracker.add(1)
        tracker.add(3)
        self.assertEqual(tracker.median(), 2.0)

    def test_duplicates(self):
        tracker = MedianTracker()
        for value in (2, 2, 2):
            tracker.add(value)
        self.assertEqual(tracker.median(), 2)

    def test_duplicates_straddling_middle(self):
        tracker = MedianTracker()
        for value in (1, 2, 2, 3):
            tracker.add(value)
        self.assertEqual(tracker.median(), 2.0)

    def test_negative_values_odd_count(self):
        tracker = MedianTracker()
        for value in (-3, -1, -2):
            tracker.add(value)
        self.assertEqual(tracker.median(), -2)

    def test_negative_values_even_count(self):
        tracker = MedianTracker()
        for value in (-4, -2, -6, -1):
            tracker.add(value)
        self.assertEqual(tracker.median(), -3.0)

    def test_interleaved_add_median(self):
        tracker = MedianTracker()
        tracker.add(10)
        self.assertEqual(tracker.median(), 10)
        tracker.add(1)
        self.assertEqual(tracker.median(), 5.5)
        tracker.add(4)
        self.assertEqual(tracker.median(), 4)
        tracker.add(7)
        self.assertEqual(tracker.median(), 5.5)

    def test_count_tracks_added_values(self):
        tracker = MedianTracker()
        self.assertEqual(tracker.count(), 0)
        tracker.add(5)
        self.assertEqual(tracker.count(), 1)
        tracker.add(3)
        tracker.add(8)
        self.assertEqual(tracker.count(), 3)

    def test_count_after_interleaved_median_calls(self):
        tracker = MedianTracker()
        tracker.add(1)
        tracker.median()
        tracker.add(2)
        tracker.median()
        tracker.add(3)
        self.assertEqual(tracker.count(), 3)


if __name__ == "__main__":
    unittest.main()
