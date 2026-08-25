import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import rle_decode, rle_encode


class RleDecodeTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(rle_decode(""), "")

    def test_doc_example(self):
        self.assertEqual(rle_decode("a3b1"), "aaab")

    def test_single_run(self):
        self.assertEqual(rle_decode("a3"), "aaa")

    def test_mixed_runs(self):
        self.assertEqual(rle_decode("a2b3c1"), "aabbbc")

    def test_multidigit_count(self):
        self.assertEqual(rle_decode("a10b2"), "aaaaaaaaaabb")

    def test_round_trip(self):
        samples = ["", "a", "abc", "aaa", "aabbbc", "aaabb", "aabbcc"]
        for text in samples:
            with self.subTest(text=text):
                self.assertEqual(rle_decode(rle_encode(text)), text)

    def test_malformed_raises(self):
        for text in ["a", "abx", "a1b", "7"]:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    rle_decode(text)


if __name__ == "__main__":
    unittest.main()
