"""Greedy word wrapping and justified text blocks without the textwrap module."""


def _tokens(text: str, width: int) -> list:
    """Split text into words, hard-breaking single words longer than width."""
    tokens = []
    for word in text.split():
        if len(word) > width:
            tokens.extend(
                word[start:start + width]
                for start in range(0, len(word), width)
            )
        else:
            tokens.append(word)
    return tokens


def wrap(text: str, width: int) -> list:
    """Greedily wrap text into lines of at most width characters.

    Words are split on runs of whitespace (tabs, newlines and spaces all
    collapse to a single gap). Any single word longer than width is hard-broken
    into width-sized chunks. Returns a list of strings; empty or all-whitespace
    text returns an empty list. Raises ValueError when width < 1.
    """
    if width < 1:
        raise ValueError("width must be positive")
    tokens = _tokens(text, width)
    lines = []
    current = []
    current_len = 0
    for token in tokens:
        if current and current_len + 1 + len(token) > width:
            lines.append(" ".join(current))
            current = [token]
            current_len = len(token)
        else:
            current.append(token)
            current_len += len(token) + (1 if current_len else 0)
    if current:
        lines.append(" ".join(current))
    return lines


def justify(text: str, width: int) -> list:
    """Return a right-justified block where every line but the last fills width.

    Extra space is distributed left-biased across the gaps between words: the
    first (gaps mod units) gaps receive one extra space. A line that cannot be
    split (a single token, or the last line) is left-aligned and returned as-is.
    Raises ValueError when width < 1.
    """
    if width < 1:
        raise ValueError("width must be positive")
    lines = wrap(text, width)
    justified = []
    for index, line in enumerate(lines):
        is_last = index == len(lines) - 1
        words = line.split(" ")
        if is_last or len(words) < 2:
            justified.append(line)
            continue
        text_len = sum(len(word) for word in words)
        gaps = len(words) - 1
        per, extra = divmod(width - text_len, gaps)
        seps = [" " * (per + 1) if i < extra else " " * per for i in range(gaps)]
        result = []
        for i, word in enumerate(words):
            result.append(word)
            if i < gaps:
                result.append(seps[i])
        justified.append("".join(result))
    return justified
