import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab import anagrams


class AnagramsTest(unittest.TestCase):
    def test_no_matches(self):
        self.assertEqual(anagrams("listen", ["hello", "world", "litten"]), [])

    def test_simple_anagram(self):
        self.assertEqual(anagrams("listen", ["enlists", "google", "silent"]), ["silent"])

    def test_case_insensitive_match(self):
        self.assertEqual(anagrams("listen", ["LISTEN", "inlets", "enlist"]), ["inlets", "enlist"])

    def test_word_never_counts_as_own_anagram(self):
        self.assertEqual(anagrams("listen", ["listen", "LISTEN", "silent"]), ["silent"])

    def test_exact_same_word_excluded(self):
        self.assertEqual(anagrams("banana", ["banana"]), [])

    def test_empty_candidates(self):
        self.assertEqual(anagrams("listen", []), [])

    def test_multiple_anagrams(self):
        self.assertEqual(
            anagrams("listen", ["silent", "listen", "tinsel", "inlets", "hello"]),
            ["silent", "tinsel", "inlets"],
        )


if __name__ == "__main__":
    unittest.main()
