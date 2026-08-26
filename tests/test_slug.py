import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.slug import slugify


class SlugifyTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(slugify(""), "")

    def test_all_punctuation(self):
        self.assertEqual(slugify("!!--..,??"), "")

    def test_lowercases_input(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_accent_folding(self):
        self.assertEqual(
            slugify("àáâãäå æ ç èéêë ìíîï ñ òóôõö ø ùúûü ý ß"),
            "aaaaaa-ae-c-eeee-iiii-n-ooooo-o-uuuu-y-ss",
        )

    def test_run_collapsing(self):
        self.assertEqual(slugify("a !!! b ... c"), "a-b-c")

    def test_trimming(self):
        self.assertEqual(slugify("  hello--  world  "), "hello-world")

    def test_numbers_kept(self):
        self.assertEqual(slugify("hello 123 world"), "hello-123-world")

    def test_cut_at_dash_within_limit(self):
        self.assertEqual(
            slugify("aaa bbb ccc ddd eee fff ggg hhh iiii", max_len=20),
            "aaa-bbb-ccc-ddd-eee",
        )

    def test_hard_cut_single_long_word(self):
        self.assertEqual(slugify("abcdefghijklmnopqrstuvwxyz", max_len=10), "abcdefghij")

    def test_no_split_at_max_len_boundary(self):
        slug = slugify("aaa bbb ccc", max_len=7)
        self.assertEqual(slug, "aaa-bbb")

    def test_max_len_validation(self):
        for bad in (0, -1, -5):
            with self.assertRaises(ValueError):
                slugify("hello", max_len=bad)

    def test_idempotence(self):
        for text in ("Hello World", " à la Crème ", "!!!", "café au lait", "already-a-slug"):
            for max_len in (1, 5, 10, 64):
                first = slugify(text, max_len=max_len)
                self.assertEqual(slugify(first, max_len=max_len), first)


if __name__ == "__main__":
    unittest.main()
