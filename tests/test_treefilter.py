import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.treefilter import filter_paths


class TreefilterTest(unittest.TestCase):
    def test_empty_allow_keeps_everything(self):
        paths = ["a.py", "b.txt", "dir/c.py"]
        self.assertEqual(filter_paths(paths, [], []), paths)

    def test_empty_allow_respects_deny(self):
        self.assertEqual(filter_paths(["a.py", "b.txt"], [], ["*.txt"]), ["a.py"])

    def test_matches_any_allow(self):
        self.assertEqual(
            filter_paths(["a.py", "b.txt", "c.py"], ["*.py"], []),
            ["a.py", "c.py"],
        )

    def test_paths_not_matching_any_allow_are_removed(self):
        self.assertEqual(filter_paths(["a.py", "b.txt"], ["*.py"], []), ["a.py"])

    def test_deny_wins_over_allow(self):
        self.assertEqual(
            filter_paths(["a.py", "b.py"], ["*.py"], ["b.py"]), ["a.py"]
        )

    def test_input_order_is_preserved(self):
        paths = ["z.txt", "a.py", "m.txt", "b.doc"]
        self.assertEqual(
            filter_paths(paths, ["*.py", "*.txt"], []), ["z.txt", "a.py", "m.txt"]
        )

    def test_multiple_allow_patterns(self):
        self.assertEqual(
            filter_paths(["a.py", "b.js", "c.go"], ["*.py", "*.go"], []),
            ["a.py", "c.go"],
        )

    def test_multiple_deny_patterns(self):
        self.assertEqual(
            filter_paths(
                ["a.py", "b.txt", "c.test.py", "d.py"],
                ["*.py"],
                ["*.test.py", "b.*"],
            ),
            ["a.py", "d.py"],
        )

    def test_deny_pattern_can_be_directories(self):
        self.assertEqual(
            filter_paths(
                ["src/util.py", "tests/util.py", "src/main.py"],
                ["**/util.py", "**/main.py"],
                ["tests/**"],
            ),
            ["src/util.py", "src/main.py"],
        )

    def test_deny_with_empty_allow(self):
        self.assertEqual(
            filter_paths(["a.py", "b.py"], [], ["b.py"]), ["a.py"]
        )

    def test_deny_does_not_apply_if_no_match(self):
        self.assertEqual(
            filter_paths(["a.py", "b.py"], [], ["c.py"]), ["a.py", "b.py"]
        )


if __name__ == "__main__":
    unittest.main()
