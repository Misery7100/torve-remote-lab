import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.csvlite import parse_csv, render_csv


class ParseCsvTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(parse_csv(""), [])

    def test_single_row(self):
        self.assertEqual(parse_csv("a,b,c"), [["a", "b", "c"]])

    def test_multiple_rows(self):
        self.assertEqual(parse_csv("a,b\nc,d"), [["a", "b"], ["c", "d"]])

    def test_quoted_comma(self):
        self.assertEqual(parse_csv('"a,b",c'), [["a,b", "c"]])

    def test_escaped_quote(self):
        self.assertEqual(parse_csv('"a""b",c'), [['a"b', "c"]])

    def test_embedded_newline(self):
        self.assertEqual(parse_csv('"a\nb",c'), [["a\nb", "c"]])

    def test_crlf(self):
        self.assertEqual(parse_csv("a,b\r\nc,d"), [["a", "b"], ["c", "d"]])

    def test_empty_fields(self):
        self.assertEqual(parse_csv("a,,c"), [["a", "", "c"]])
        self.assertEqual(parse_csv(",a"), [["", "a"]])
        self.assertEqual(parse_csv("a,"), [["a", ""]])
        self.assertEqual(parse_csv(","), [["", ""]])

    def test_quoted_empty_field(self):
        self.assertEqual(parse_csv('"",a'), [["", "a"]])

    def test_trailing_newline_is_terminator(self):
        self.assertEqual(parse_csv("a,b\n"), [["a", "b"]])
        self.assertEqual(parse_csv("a,b\r\n"), [["a", "b"]])

    def test_unterminated_quoted_field_raises(self):
        with self.assertRaises(ValueError):
            parse_csv('"abc')

    def test_char_after_quote_raises(self):
        with self.assertRaises(ValueError):
            parse_csv('"a"x')


class RenderCsvTest(unittest.TestCase):
    def test_plain_fields_not_quoted(self):
        self.assertEqual(render_csv([["a", "b", "c"]]), "a,b,c")

    def test_comma_field_is_quoted(self):
        self.assertEqual(render_csv([["a,b"]]), '"a,b"')

    def test_quote_field_is_quoted_and_escaped(self):
        self.assertEqual(render_csv([['a"b']]), '"a""b"')

    def test_newline_field_is_quoted(self):
        self.assertEqual(render_csv([["a\nb"]]), '"a\nb"')

    def test_quote_only_when_needed(self):
        self.assertEqual(render_csv([["a", "b,c", "d"]]), 'a,"b,c",d')


class RoundTripTest(unittest.TestCase):
    def test_round_trip(self):
        rows = [
            ["a", "b", "c"],
            ["a,b", 'a"b', "a\nb"],
            ["", "", ""],
            ["x", "", "y"],
        ]
        self.assertEqual(parse_csv(render_csv(rows)), rows)

    def test_round_trip_single_empty_field_within_row(self):
        rows = [["a", ""], ["", "b"]]
        self.assertEqual(parse_csv(render_csv(rows)), rows)


if __name__ == "__main__":
    unittest.main()
