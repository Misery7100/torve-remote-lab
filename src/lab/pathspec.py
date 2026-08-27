"""A stdlib-only gitwildmatch-style matcher for forward-slash relative paths."""

import re


def match(pattern: str, path: str) -> bool:
    """Return True when ``path`` matches glob ``pattern``.

    The glob uses forward slashes as the segment separator and supports:

    * ``*``  - any run of characters within a segment (never ``/``)
    * ``?``  - exactly one non-slash character
    * ``**`` - as a whole segment, any number of segments including zero
    * ``[...]`` - a character class with ranges and optional ``!``/``^`` negation

    An empty ``pattern`` or an unterminated character class raises ``ValueError``.
    """
    if pattern == "":
        raise ValueError("pattern must not be empty")
    regex = _translate(pattern)
    return re.fullmatch(regex, path) is not None


def _translate(pattern: str) -> str:
    n = len(pattern)
    out = []
    i = 0
    while i < n:
        c = pattern[i]
        if c == "*":
            if i + 1 < n and pattern[i + 1] == "*":
                start_ok = (i == 0) or (pattern[i - 1] == "/")
                end_ok = (i + 2 == n) or (pattern[i + 2] == "/")
                if start_ok and end_ok:
                    if i + 2 == n:
                        if i == 0:
                            return ".*"
                        out.append("(?:/[^/]+)*")
                        i += 2
                        continue
                    # followed by a '/', consumed as part of the leading term
                    out.append("(?:[^/]+/)*")
                    i += 3
                    continue
            out.append("[^/]*")
            i += 1
            continue
        if c == "?":
            out.append("[^/]")
            i += 1
            continue
        if c == "/":
            # A '/' directly before a whole-segment '**' is part of that term.
            if i + 2 < n and pattern[i + 1:i + 3] == "**":
                whole_after = (i + 3 == n) or (pattern[i + 3] == "/")
                if whole_after:
                    out.append("(?:/[^/]+)*")
                    i += 3
                    continue
            out.append("/")
            i += 1
            continue
        if c == "[":
            cls, i = _parse_class(pattern, i)
            out.append(cls)
            continue
        out.append(re.escape(c))
        i += 1
    return "".join(out)


def _parse_class(pattern: str, start: int) -> tuple[str, int]:
    n = len(pattern)
    i = start + 1
    negate = False
    if i < n and pattern[i] in ("!", "^"):
        negate = True
        i += 1
    items = []
    closed = False
    if i < n and pattern[i] == "]":
        items.append(r"\]")
        i += 1
    while i < n:
        ch = pattern[i]
        if ch == "]":
            closed = True
            i += 1
            break
        if ch == "\\":
            items.append(r"\\")
            i += 1
            if i < n:
                items.append(re.escape(pattern[i]))
                i += 1
            continue
        items.append(ch)
        i += 1
    if not closed:
        raise ValueError("unterminated character class")
    body = "".join(items).replace("[", r"\[")
    return "[" + ("^" if negate else "") + body + "]", i
