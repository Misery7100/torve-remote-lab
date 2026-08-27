import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.pathspec import match


class PathspecTest(unittest.TestCase):
    def test_exact_match(self):
        self.assertTrue(match("foo", "foo"))
        self.assertFalse(match("foo", "bar"))
        self.assertFalse(match("foo", "fo"))

    def test_star_within_segment(self):
        self.assertTrue(match("*.py", "main.py"))
        self.assertFalse(match("*.py", "main.pyc"))
        self.assertFalse(match("*.py", "dir/main.py"))

    def test_star_does_not_cross_segments(self):
        self.assertFalse(match("a*b", "a/x/b"))
        self.assertFalse(match("a*", "a/b"))

    def test_question_mark_single_non_slash(self):
        self.assertTrue(match("a?c", "abc"))
        self.assertFalse(match("a?c", "ac"))
        self.assertFalse(match("a?c", "a/c"))

    def test_question_mark_in_path(self):
        self.assertTrue(match("foo/???.py", "foo/abc.py"))
        self.assertFalse(match("foo/???.py", "foo/abcdef.py"))

    def test_double_star_leading(self):
        self.assertTrue(match("**/foo", "foo"))
        self.assertTrue(match("**/foo", "a/foo"))
        self.assertTrue(match("**/foo", "a/b/foo"))
        self.assertFalse(match("**/foo", "a/b/foobar"))

    def test_double_star_trailing(self):
        self.assertTrue(match("foo/**", "foo"))
        self.assertTrue(match("foo/**", "foo/a"))
        self.assertTrue(match("foo/**", "foo/a/b"))
        self.assertFalse(match("foo/**", "bar/a"))

    def test_double_star_middle(self):
        self.assertTrue(match("a/**/b", "a/b"))
        self.assertTrue(match("a/**/b", "a/x/b"))
        self.assertTrue(match("a/**/b", "a/x/y/b"))
        self.assertFalse(match("a/**/b", "a/b/c"))

    def test_double_star_alone(self):
        self.assertTrue(match("**", "anything"))
        self.assertTrue(match("**", "a/b/c/deep"))

    def test_literals_are_escaped(self):
        self.assertTrue(match("a.b", "a.b"))
        self.assertFalse(match("a.b", "axb"))

    def test_character_class_simple(self):
        self.assertTrue(match("file[0-9].txt", "file1.txt"))
        self.assertFalse(match("file[0-9].txt", "filex.txt"))

    def test_character_class_letter_range(self):
        self.assertTrue(match("[a-c]x", "ax"))
        self.assertTrue(match("[a-c]x", "cx"))
        self.assertFalse(match("[a-c]x", "dx"))

    def test_character_class_negated_bang(self):
        self.assertTrue(match("[!0-9]", "a"))
        self.assertFalse(match("[!0-9]", "5"))

    def test_character_class_negated_caret(self):
        self.assertTrue(match("[^0-9]", "a"))
        self.assertFalse(match("[^0-9]", "5"))

    def test_character_class_multiple(self):
        self.assertTrue(match("[abc]", "a"))
        self.assertTrue(match("[abc]", "c"))
        self.assertFalse(match("[abc]", "d"))

    def test_class_within_pattern(self):
        self.assertTrue(match("dir/[ab]/x", "dir/a/x"))
        self.assertTrue(match("dir/[ab]/x", "dir/b/x"))
        self.assertFalse(match("dir/[ab]/x", "dir/c/x"))

    def test_empty_pattern_raises(self):
        with self.assertRaises(ValueError):
            match("", "foo")

    def test_unterminated_class_raises(self):
        for bad in ("[abc", "a/[def", "[]"):
            with self.assertRaises(ValueError):
                match(bad, "foo")


if __name__ == "__main__":
    unittest.main()
