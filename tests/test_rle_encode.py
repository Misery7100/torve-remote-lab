import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import rle_encode


class RleEncodeTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(rle_encode(""), "")

    def test_single_character(self):
        self.assertEqual(rle_encode("a"), "a1")

    def test_no_repeats(self):
        self.assertEqual(rle_encode("abc"), "a1b1c1")

    def test_single_run(self):
        self.assertEqual(rle_encode("aaa"), "a3")

    def test_mixed_runs(self):
        self.assertEqual(rle_encode("aabbbc"), "a2b3c1")

    def test_doc_example(self):
        self.assertEqual(rle_encode("aaabb"), "a3b2")

    def test_repeated_single_character(self):
        self.assertEqual(rle_encode("aabbcc"), "a2b2c2")


if __name__ == "__main__":
    unittest.main()
