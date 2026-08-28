import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.rangeset import RangeSet


class AddTest(unittest.TestCase):
    def test_add_to_empty(self):
        rs = RangeSet()
        rs.add(1, 5)
        self.assertEqual(rs.ranges(), [(1, 5)])

    def test_add_disjoint_descending_sorted(self):
        rs = RangeSet()
        rs.add(5, 8)
        rs.add(1, 3)
        self.assertEqual(rs.ranges(), [(1, 3), (5, 8)])

    def test_add_merges_overlap(self):
        rs = RangeSet()
        rs.add(1, 5)
        rs.add(3, 8)
        self.assertEqual(rs.ranges(), [(1, 8)])

    def test_add_merges_adjacent(self):
        rs = RangeSet()
        rs.add(1, 3)
        rs.add(3, 5)
        self.assertEqual(rs.ranges(), [(1, 5)])

    def test_add_contained_range(self):
        rs = RangeSet()
        rs.add(1, 10)
        rs.add(2, 5)
        self.assertEqual(rs.ranges(), [(1, 10)])

    def test_add_bridges_two_ranges(self):
        rs = RangeSet()
        rs.add(1, 3)
        rs.add(7, 9)
        rs.add(3, 7)
        self.assertEqual(rs.ranges(), [(1, 9)])

    def test_add_merges_multiple_cascade(self):
        rs = RangeSet()
        rs.add(1, 2)
        rs.add(4, 5)
        rs.add(6, 8)
        rs.add(2, 6)
        self.assertEqual(rs.ranges(), [(1, 8)])

    def test_add_does_not_merge_nonadjacent(self):
        rs = RangeSet()
        rs.add(1, 3)
        rs.add(5, 7)
        self.assertEqual(rs.ranges(), [(1, 3), (5, 7)])

    def test_add_extend_left(self):
        rs = RangeSet()
        rs.add(3, 5)
        rs.add(1, 4)
        self.assertEqual(rs.ranges(), [(1, 5)])

    def test_add_extend_right(self):
        rs = RangeSet()
        rs.add(1, 3)
        rs.add(2, 6)
        self.assertEqual(rs.ranges(), [(1, 6)])

    def test_add_duplicate(self):
        rs = RangeSet()
        rs.add(1, 5)
        rs.add(1, 5)
        self.assertEqual(rs.ranges(), [(1, 5)])


class AddValidationTest(unittest.TestCase):
    def test_add_empty_range_raises(self):
        rs = RangeSet()
        with self.assertRaises(ValueError):
            rs.add(3, 3)

    def test_add_inverted_range_raises(self):
        rs = RangeSet()
        with self.assertRaises(ValueError):
            rs.add(5, 2)


class ContainsTest(unittest.TestCase):
    def setUp(self):
        self.rs = RangeSet()
        self.rs.add(1, 5)
        self.rs.add(10, 13)

    def test_inside_range(self):
        self.assertTrue(self.rs.contains(3))

    def test_first_inclusive(self):
        self.assertTrue(self.rs.contains(1))

    def test_stop_exclusive(self):
        self.assertFalse(self.rs.contains(5))

    def test_before_all(self):
        self.assertFalse(self.rs.contains(0))

    def test_gap(self):
        self.assertFalse(self.rs.contains(7))

    def test_second_range(self):
        self.assertTrue(self.rs.contains(10))

    def test_in_second_range(self):
        self.assertTrue(self.rs.contains(12))

    def test_after_all(self):
        self.assertFalse(self.rs.contains(20))


class ContainsEmptyTest(unittest.TestCase):
    def test_empty_contains_nothing(self):
        rs = RangeSet()
        self.assertFalse(rs.contains(0))
        self.assertFalse(rs.contains(100))


class RangesTest(unittest.TestCase):
    def test_empty_ranges(self):
        self.assertEqual(RangeSet().ranges(), [])

    def test_ranges_returns_copy(self):
        rs = RangeSet()
        rs.add(1, 3)
        result = rs.ranges()
        result.append((9, 10))
        self.assertEqual(rs.ranges(), [(1, 3)])


class TotalTest(unittest.TestCase):
    def test_total_empty(self):
        self.assertEqual(RangeSet().total(), 0)

    def test_total_single_range(self):
        rs = RangeSet()
        rs.add(1, 5)
        self.assertEqual(rs.total(), 4)

    def test_total_after_merge(self):
        rs = RangeSet()
        rs.add(1, 5)
        rs.add(3, 9)
        self.assertEqual(rs.total(), 8)

    def test_total_multiple_disjoint(self):
        rs = RangeSet()
        rs.add(1, 5)
        rs.add(10, 13)
        self.assertEqual(rs.total(), 7)

    def test_total_union_of_adjacent(self):
        rs = RangeSet()
        rs.add(1, 3)
        rs.add(3, 5)
        self.assertEqual(rs.total(), 4)


if __name__ == "__main__":
    unittest.main()
