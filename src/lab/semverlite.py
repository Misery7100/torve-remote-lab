import re


_NUMBER_RE = re.compile(r"^0$|^[1-9][0-9]*$")
_ALNUM_RE = re.compile(r"^[0-9A-Za-z-]+$")


def _parse_identifier(identifier):
    if not identifier:
        raise ValueError("empty identifier")
    if identifier.isdigit():
        if _NUMBER_RE.match(identifier) is None:
            raise ValueError(f"leading zero in numeric identifier: {identifier!r}")
        return ("numeric", int(identifier))
    if _ALNUM_RE.match(identifier) is None:
        raise ValueError(f"invalid identifier: {identifier!r}")
    return ("alphanumeric", identifier)


def parse_semver(text):
    """Parse a SemVer 2.0.0 string (without build metadata).

    Returns (major, minor, patch, prerelease_identifiers_tuple). The
    prerelease tuple is empty when the version has no prerelease. Raises
    ValueError on leading zeros in numeric parts, empty identifiers, or
    malformed input.
    """
    if not isinstance(text, str):
        raise ValueError("input must be a string")

    core, separator, prerelease = text.partition("-")
    if not separator:
        prerelease = ""

    parts = core.split(".")
    if len(parts) != 3:
        raise ValueError(f"malformed version: {text!r}")
    numbers = []
    for part in parts:
        if not part.isdigit():
            raise ValueError(f"malformed numeric part: {part!r}")
        if _NUMBER_RE.match(part) is None:
            raise ValueError(f"leading zero in numeric part: {part!r}")
        numbers.append(int(part))

    ids = []
    if separator:
        for identifier in prerelease.split("."):
            ids.append(_parse_identifier(identifier))

    return numbers[0], numbers[1], numbers[2], tuple(ids)


def _compare_identifiers(a, b):
    if a[0] == "numeric" and b[0] == "numeric":
        a_val = a[1]
        b_val = b[1]
        return (a_val > b_val) - (a_val < b_val)
    if a[0] == "numeric":
        return -1
    if b[0] == "numeric":
        return 1
    return (a[1] > b[1]) - (a[1] < b[1])


def compare_semver(a, b):
    """Compare two SemVer version strings; return -1, 0, or 1.

    Implements SemVer 2.0.0 precedence without build metadata.
    """
    amaj, amin, apat, apre = parse_semver(a)
    bmaj, bmin, bpat, bpre = parse_semver(b)

    core = ((amaj > bmaj) - (amaj < bmaj)) or ((amin > bmin) - (amin < bmin)) or ((apat > bpat) - (apat < bpat))
    if core:
        return core

    if not apre and not bpre:
        return 0
    if not apre:
        return 1
    if not bpre:
        return -1

    for ia, ib in zip(apre, bpre):
        result = _compare_identifiers(ia, ib)
        if result:
            return result
    if len(apre) == len(bpre):
        return 0
    return -1 if len(apre) < len(bpre) else 1
