import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.urlq import format_qs, parse_qs


class ParseQsTest(unittest.TestCase):
    def test_empty_query(self):
        self.assertEqual(parse_qs(""), [])

    def test_simple_single_pair(self):
        self.assertEqual(parse_qs("a=1"), [("a", "1")])

    def test_multiple_pairs(self):
        self.assertEqual(parse_qs("a=1&b=2&c=3"), [("a", "1"), ("b", "2"), ("c", "3")])

    def test_duplicate_keys_preserved(self):
        self.assertEqual(parse_qs("x=1&x=2&x=3"), [("x", "1"), ("x", "2"), ("x", "3")])

    def test_order_preserved(self):
        self.assertEqual(parse_qs("b=2&a=1&c=3"), [("b", "2"), ("a", "1"), ("c", "3")])

    def test_pair_with_no_equals_has_empty_value(self):
        self.assertEqual(parse_qs("flag"), [("flag", "")])

    def test_pair_with_empty_key_is_skipped(self):
        self.assertEqual(parse_qs("&a=1&"), [("a", "1")])

    def test_pair_with_empty_key_and_value_is_skipped(self):
        self.assertEqual(parse_qs("=x&a=1"), [("a", "1")])

    def test_empty_value_with_equals(self):
        self.assertEqual(parse_qs("a="), [("a", "")])

    def test_value_containing_equals(self):
        self.assertEqual(parse_qs("a=b=c&d=e"), [("a", "b=c"), ("d", "e")])

    def test_plus_decodes_to_space(self):
        self.assertEqual(parse_qs("a=hello%20world"), [("a", "hello world")])

    def test_plus_in_key_and_value(self):
        self.assertEqual(parse_qs("a+b=1+2"), [("a b", "1 2")])

    def test_percent_escape_hex(self):
        self.assertEqual(parse_qs("a=1%2b1"), [("a", "1+1")])

    def test_percent_escape_mixed_case(self):
        self.assertEqual(parse_qs("a=%2f%2F%2f"), [("a", "///")])

    def test_percent_escape_lowercase(self):
        self.assertEqual(parse_qs("a=%c3%af"), [("a", "ï")])

    def test_utf8_multibyte_percent_sequences(self):
        self.assertEqual(parse_qs("a=%e2%82%ac"), [("a", "€")])

    def test_truncated_percent_escape_raises(self):
        with self.assertRaises(ValueError):
            parse_qs("a=%")

    def test_truncated_percent_escape_one_digit_raises(self):
        with self.assertRaises(ValueError):
            parse_qs("a=%2")

    def test_non_hex_percent_escape_raises(self):
        with self.assertRaises(ValueError):
            parse_qs("a=%GG")

    def test_non_hex_second_digit_raises(self):
        with self.assertRaises(ValueError):
            parse_qs("a=%2G")


class FormatQsTest(unittest.TestCase):
    def test_empty_pairs(self):
        self.assertEqual(format_qs([]), "")

    def test_simple(self):
        self.assertEqual(format_qs([("a", "1"), ("b", "2")]), "a=1&b=2")

    def test_space_encodes_as_plus(self):
        self.assertEqual(format_qs([("a b", "1 2")]), "a+b=1+2")

    def test_reserved_chars_are_escaped(self):
        self.assertEqual(format_qs([("a&b=c", "x&y=z")]), "a%26b%3Dc=x%26y%3Dz")

    def test_percent_is_escaped(self):
        self.assertEqual(format_qs([("p", "50%")]), "p=50%25")

    def test_plus_is_escaped(self):
        self.assertEqual(format_qs([("p", "a+b")]), "p=a%2Bb")

    def test_uppercase_hex(self):
        self.assertEqual(format_qs([("a", "\n")]), "a=%0A")


class RoundTripTest(unittest.TestCase):
    def test_round_trip_order_and_duplicates(self):
        pairs = [("b", "2"), ("a", "1"), ("b", "3"), ("x", ""), ("s", "sp ace&=%+"), ("k", "ünï")]
        self.assertEqual(parse_qs(format_qs(pairs)), pairs)

    def test_round_trip_utf8(self):
        pairs = [("k", "héllo wörld € 你好")]
        self.assertEqual(parse_qs(format_qs(pairs)), pairs)

    def test_round_trip_empty_then_some(self):
        pairs = [("", "v"), ("a", "1")]
        self.assertEqual(parse_qs(format_qs(pairs)), [("a", "1")])

    def test_format_then_parse_of_static(self):
        self.assertEqual(parse_qs(format_qs([("a", "b=c"), ("d", "e f")])), [("a", "b=c"), ("d", "e f")])


if __name__ == "__main__":
    unittest.main()
