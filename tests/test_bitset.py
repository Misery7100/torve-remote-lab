import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.bitset import BitSet


class BitSetConstructionTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(len(BitSet()), 0)
        self.assertFalse(BitSet())

    def test_construction(self):
        self.assertEqual(BitSet([1, 5, 9])._mask, 0b1000100010)

    def test_dedup_on_construction(self):
        self.assertEqual(list(BitSet([3, 1, 3, 1])), [1, 3])

    def test_rejects_negative(self):
        with self.assertRaises(ValueError):
            BitSet([1, -2])
        with self.assertRaises(ValueError):
            BitSet().add(-1)
        with self.assertRaises(ValueError):
            BitSet().discard(-1)

    def test_rejects_non_int(self):
        with self.assertRaises(ValueError):
            BitSet([1, "a"])
        with self.assertRaises(ValueError):
            BitSet().add(1.5)
        with self.assertRaises(ValueError):
            1.5 in BitSet()

    def test_rejects_bool(self):
        with self.assertRaises(ValueError):
            BitSet([True])
        with self.assertRaises(ValueError):
            BitSet().add(True)
        with self.assertRaises(ValueError):
            False in BitSet()


class BitSetMembershipTest(unittest.TestCase):
    def test_contains(self):
        b = BitSet([1, 5])
        self.assertIn(1, b)
        self.assertIn(5, b)
        self.assertNotIn(3, b)

    def test_len_popcount(self):
        self.assertEqual(len(BitSet([0, 4, 9, 1, 9])), 4)


class BitSetIterationTest(unittest.TestCase):
    def test_ascending_order(self):
        self.assertEqual(list(BitSet([9, 1, 5])), [1, 5, 9])

    def test_iter_empty(self):
        self.assertEqual(list(BitSet()), [])


class BitSetMutationTest(unittest.TestCase):
    def test_add_discard(self):
        b = BitSet([1, 5])
        b.add(2)
        self.assertEqual(list(b), [1, 2, 5])
        b.discard(5)
        self.assertEqual(list(b), [1, 2])

    def test_discard_absent_is_silent(self):
        b = BitSet([1, 5])
        b.discard(3)
        self.assertEqual(list(b), [1, 5])

    def test_clear(self):
        b = BitSet([1, 5, 9])
        b.clear()
        self.assertFalse(b)
        self.assertEqual(len(b), 0)
        self.assertEqual(list(b), [])


class BitSetEqualityTest(unittest.TestCase):
    def test_equal_sets(self):
        self.assertEqual(BitSet([1, 5]), BitSet([5, 1]))

    def test_unequal_sets(self):
        self.assertNotEqual(BitSet([1, 5]), BitSet([1, 6]))

    def test_not_equal_to_other_type(self):
        self.assertNotEqual(BitSet([1, 5]), [1, 5])


class BitSetOperationsTest(unittest.TestCase):
    def test_union(self):
        self.assertEqual(list(BitSet([1, 2]).union(BitSet([2, 3]))), [1, 2, 3])

    def test_intersection(self):
        self.assertEqual(list(BitSet([1, 2, 3]).intersection(BitSet([2, 3, 4]))), [2, 3])

    def test_union_leaves_operands_untouched(self):
        a = BitSet([1, 2])
        b = BitSet([2, 3])
        a.union(b)
        self.assertEqual(list(a), [1, 2])
        self.assertEqual(list(b), [2, 3])

    def test_intersection_leaves_operands_untouched(self):
        a = BitSet([1, 2, 3])
        b = BitSet([2, 3, 4])
        a.intersection(b)
        self.assertEqual(list(a), [1, 2, 3])
        self.assertEqual(list(b), [2, 3, 4])

    def test_union_mutual_exclusive(self):
        self.assertEqual(
            list(BitSet([1, 2]).union(BitSet([3, 4]))),
            [1, 2, 3, 4],
        )

    def test_intersection_disjoint_is_empty(self):
        self.assertFalse(BitSet([1]).intersection(BitSet([2])))


class BitSetTruthinessTest(unittest.TestCase):
    def test_empty_falsy(self):
        self.assertFalse(BitSet())

    def test_nonempty_truthy(self):
        self.assertTrue(BitSet([0]))

    def test_after_clear_falsy(self):
        b = BitSet([1, 5, 9])
        b.clear()
        self.assertFalse(b)


class BitSetReprTest(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(BitSet([9, 1, 5])), "BitSet([1, 5, 9])")

    def test_repr_empty(self):
        self.assertEqual(repr(BitSet()), "BitSet([])")


if __name__ == "__main__":
    unittest.main()
