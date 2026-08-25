import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.intervals import merge_intervals, subtract_intervals


class MergeIntervalsTest(unittest.TestCase):
    def test_overlap(self):
        self.assertEqual(merge_intervals([(1, 5), (3, 8)]), [(1, 8)])

    def test_adjacency_merges(self):
        self.assertEqual(merge_intervals([(1, 3), (3, 5)]), [(1, 5)])

    def test_containment(self):
        self.assertEqual(merge_intervals([(1, 10), (2, 5)]), [(1, 10)])

    def test_disjoint_sorted(self):
        self.assertEqual(merge_intervals([(5, 8), (1, 3)]), [(1, 3), (5, 8)])

    def test_empty_input(self):
        self.assertEqual(merge_intervals([]), [])

    def test_single_interval(self):
        self.assertEqual(merge_intervals([(2, 4)]), [(2, 4)])

    def test_unsorted_input(self):
        self.assertEqual(merge_intervals([(8, 9), (1, 6), (3, 9)]), [(1, 9)])

    def test_start_equal_end_raises(self):
        with self.assertRaises(ValueError):
            merge_intervals([(3, 3)])

    def test_start_greater_than_end_raises(self):
        with self.assertRaises(ValueError):
            merge_intervals([(5, 2)])


class SubtractIntervalsTest(unittest.TestCase):
    def test_disjoint_holes(self):
        self.assertEqual(subtract_intervals([(1, 10)], [(2, 3)]), [(1, 2), (3, 10)])

    def test_hole_is_disjoint_no_op(self):
        self.assertEqual(subtract_intervals([(1, 5)], [(6, 8)]), [(1, 5)])

    def test_contained_hole_covers_all(self):
        self.assertEqual(subtract_intervals([(2, 8)], [(1, 10)]), [])

    def test_hole_covers_exactly_in_interval(self):
        self.assertEqual(subtract_intervals([(1, 10)], [(1, 10)]), [])

    def test_partial_hole_splits_interval(self):
        self.assertEqual(subtract_intervals([(1, 10)], [(4, 6)]), [(1, 4), (6, 10)])

    def test_hole_covers_left_edge(self):
        self.assertEqual(subtract_intervals([(1, 10)], [(1, 5)]), [(5, 10)])

    def test_hole_covers_right_edge(self):
        self.assertEqual(subtract_intervals([(1, 10)], [(5, 10)]), [(1, 5)])

    def test_multiple_holes(self):
        self.assertEqual(
            subtract_intervals([(1, 10)], [(2, 3), (7, 9)]),
            [(1, 2), (3, 7), (9, 10)],
        )

    def test_multiple_base_intervals(self):
        self.assertEqual(
            subtract_intervals([(1, 5), (10, 15)], [(3, 12)]),
            [(1, 3), (12, 15)],
        )

    def test_holes_full_cover_multiple(self):
        self.assertEqual(subtract_intervals([(1, 5), (10, 15)], [(1, 20)]), [])

    def test_empty_base(self):
        self.assertEqual(subtract_intervals([], [(1, 3)]), [])

    def test_empty_holes(self):
        self.assertEqual(subtract_intervals([(1, 3)], []), [(1, 3)])

    def test_both_empty(self):
        self.assertEqual(subtract_intervals([], []), [])

    def test_start_equal_end_hole_raises(self):
        with self.assertRaises(ValueError):
            subtract_intervals([(1, 10)], [(5, 5)])

    def test_start_greater_than_end_base_raises(self):
        with self.assertRaises(ValueError):
            subtract_intervals([(10, 1)], [(2, 3)])


if __name__ == "__main__":
    unittest.main()
