import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lab.semverlite import compare_semver, parse_semver


class ParseSemverTest(unittest.TestCase):
    def test_plain_core(self):
        self.assertEqual(parse_semver("1.2.3"), (1, 2, 3, ()))

    def test_zeros_in_core(self):
        self.assertEqual(parse_semver("0.0.0"), (0, 0, 0, ()))

    def test_large_numbers(self):
        self.assertEqual(parse_semver("10.20.300"), (10, 20, 300, ()))

    def test_prerelease_single_numeric(self):
        self.assertEqual(parse_semver("1.0.0-alpha"), (1, 0, 0, (("alphanumeric", "alpha"),)))

    def test_prerelease_multiple(self):
        self.assertEqual(
            parse_semver("1.0.0-alpha.1.beta"),
            (1, 0, 0, (("alphanumeric", "alpha"), ("numeric", 1), ("alphanumeric", "beta"))),
        )

    def test_prerelease_numeric_zero(self):
        self.assertEqual(parse_semver("1.0.0-0"), (1, 0, 0, (("numeric", 0),)))

    def test_prerelease_with_dash(self):
        self.assertEqual(parse_semver("1.0.0-rc-1"), (1, 0, 0, (("alphanumeric", "rc-1"),)))

    def test_core_leading_zero_raises(self):
        with self.assertRaises(ValueError):
            parse_semver("01.2.3")

    def test_core_leading_zero_minor_raises(self):
        with self.assertRaises(ValueError):
            parse_semver("1.02.3")

    def test_core_leading_zero_patch_raises(self):
        with self.assertRaises(ValueError):
            parse_semver("1.2.03")

    def test_numeric_prerelease_leading_zero_raises(self):
        with self.assertRaises(ValueError):
            parse_semver("1.0.0-01")

    def test_too_few_parts_raises(self):
        with self.assertRaises(ValueError):
            parse_semver("1.2")

    def test_too_many_parts_raises(self):
        with self.assertRaises(ValueError):
            parse_semver("1.2.3.4")

    def test_non_numeric_core_raises(self):
        with self.assertRaises(ValueError):
            parse_semver("a.b.c")

    def test_empty_part_raises(self):
        with self.assertRaises(ValueError):
            parse_semver("1..3")

    def test_empty_identifier_raises(self):
        with self.assertRaises(ValueError):
            parse_semver("1.0.0-alpha..1")

    def test_trailing_empty_identifier_raises(self):
        with self.assertRaises(ValueError):
            parse_semver("1.0.0-alpha.")

    def test_build_metadata_is_not_accepted(self):
        with self.assertRaises(ValueError):
            parse_semver("1.0.0+build")

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            parse_semver("")

    def test_non_string_raises(self):
        with self.assertRaises(ValueError):
            parse_semver(1.0)


class SemverOrderingChainTest(unittest.TestCase):
    def test_spec_ordering_chain(self):
        chain = [
            "1.0.0-alpha",
            "1.0.0-alpha.1",
            "1.0.0-alpha.beta",
            "1.0.0-beta",
            "1.0.0-beta.2",
            "1.0.0-beta.11",
            "1.0.0-rc.1",
            "1.0.0",
        ]
        for idx, version in enumerate(chain):
            for compare_to in chain[:idx]:
                self.assertEqual(compare_semver(compare_to, version), -1, f"{compare_to} should precede {version}")
                self.assertEqual(compare_semver(version, compare_to), 1, f"{version} should follow {compare_to}")
        for version in chain:
            self.assertEqual(compare_semver(version, version), 0)


class CompareSemverTest(unittest.TestCase):
    def test_equal_core_no_prerelease(self):
        self.assertEqual(compare_semver("1.0.0", "1.0.0"), 0)

    def test_major_precedence(self):
        self.assertEqual(compare_semver("2.0.0", "1.0.0"), 1)
        self.assertEqual(compare_semver("1.0.0", "2.0.0"), -1)

    def test_minor_precedence(self):
        self.assertEqual(compare_semver("1.2.0", "1.1.0"), 1)

    def test_patch_precedence(self):
        self.assertEqual(compare_semver("1.0.1", "1.0.0"), 1)

    def test_prerelease_is_lower_than_release(self):
        self.assertEqual(compare_semver("1.0.0-alpha", "1.0.0"), -1)
        self.assertEqual(compare_semver("1.0.0", "1.0.0-alpha"), 1)

    def test_numeric_identifier_ranks_below_alphanumeric(self):
        self.assertEqual(compare_semver("1.0.0-1", "1.0.0-alpha"), -1)

    def test_numeric_identifiers_compare_numerically(self):
        self.assertEqual(compare_semver("1.0.0-beta.11", "1.0.0-beta.2"), 1)

    def test_alphanumeric_compare_as_ascii(self):
        self.assertEqual(compare_semver("1.0.0-alpha.beta", "1.0.0-alpha.alpha"), 1)

    def test_shorter_prerelease_ranks_lower(self):
        self.assertEqual(compare_semver("1.0.0-alpha", "1.0.0-alpha.1"), -1)

    def test_equal_prerelease_is_equal(self):
        self.assertEqual(compare_semver("1.0.0-beta.2", "1.0.0-beta.2"), 0)

    def test_first_differing_identifier_wins(self):
        self.assertEqual(compare_semver("1.0.0-1.alpha", "1.0.0-1.beta"), -1)


if __name__ == "__main__":
    unittest.main()
