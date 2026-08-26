import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.topo import CycleError, topo_sort


class TopoSortTest(unittest.TestCase):
    def test_empty_mapping(self):
        self.assertEqual(topo_sort({}), [])

    def test_direct_single_dependency_chain(self):
        result = topo_sort({"a": ["b"], "b": ["c"]})
        self.assertEqual(result, ["c", "b", "a"])

    def test_deterministic_tie_breaking(self):
        result = topo_sort({"b": ["d"], "c": ["d"], "a": ["d"], "d": []})
        self.assertEqual(result, ["d", "a", "b", "c"])

    def test_implicit_nodes_included(self):
        result = topo_sort({"x": ["implicit"]})
        self.assertEqual(result, ["implicit", "x"])

    def test_duplicate_dependencies_tolerated(self):
        result = topo_sort({"a": ["b", "b", "b"]})
        self.assertEqual(result, ["b", "a"])

    def test_self_loop_raises_cycle_error(self):
        with self.assertRaises(CycleError) as ctx:
            topo_sort({"a": ["a"]})
        self.assertIn("a -> a", str(ctx.exception))

    def test_cycle_error_is_value_error(self):
        self.assertTrue(issubclass(CycleError, ValueError))

    def test_longer_cycle_message(self):
        deps = {"a": ["b"], "b": ["c"], "c": ["a"], "z": []}
        with self.assertRaises(CycleError) as ctx:
            topo_sort(deps)
        msg = str(ctx.exception)
        self.assertIn("a -> b -> c -> a", msg)

    def test_only_satisfiable_nodes_returned_before_error(self):
        msg = None
        try:
            topo_sort({"a": ["b"], "b": ["c"], "c": ["a"]})
        except CycleError as exc:
            msg = str(exc)
        self.assertIn("a -> b -> c -> a", msg)


if __name__ == "__main__":
    unittest.main()
