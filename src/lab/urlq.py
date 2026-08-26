_HEX_CHARS = "0123456789abcdefABCDEF"


def _decode_bytes(segment):
    """Decode a raw query segment (no '=' split) into bytes.

    '+' decodes to a space; %XX percent-escapes decode case-insensitively.
    Raises ValueError on a malformed escape (truncated or non-hex digits).
    """
    out = bytearray()
    index = 0
    length = len(segment)
    while index < length:
        ch = segment[index]
        if ch == "+":
            out.append(0x20)
            index += 1
        elif ch == "%":
            if index + 2 > length - 1:
                raise ValueError(f"malformed percent-escape in {segment!r}")
            hi = segment[index + 1]
            lo = segment[index + 2]
            if hi not in _HEX_CHARS or lo not in _HEX_CHARS:
                raise ValueError(f"malformed percent-escape in {segment!r}")
            out.append(int(hi + lo, 16))
            index += 3
        else:
            codepoint = ord(ch)
            if codepoint > 127:
                raise ValueError(f"non-ASCII byte not percent-encoded in {segment!r}")
            out.append(codepoint)
            index += 1
    return bytes(out)


def parse_qs(query):
    """Parse a URL query string into a list of (key, value) pairs.

    Pairs are separated by '&'; a key and value are split at the first '='.
    A pair with no '=' keeps an empty value; a pair with an empty key is
    skipped. Order and duplicate keys are preserved. '+' decodes to a space
    and %XX escapes decode case-insensitively. Raises ValueError on a
    malformed percent-escape.
    """
    if not isinstance(query, str):
        raise ValueError("query must be a string")
    pairs = []
    for pair in query.split("&"):
        if "=" in pair:
            raw_key, _, raw_value = pair.partition("=")
        else:
            raw_key, raw_value = pair, ""
        if raw_key == "":
            continue
        key = _decode_bytes(raw_key).decode("utf-8")
        value = _decode_bytes(raw_value).decode("utf-8")
        pairs.append((key, value))
    return pairs


_ALWAYS_ESCAPED = frozenset("&=%+")


def format_qs(pairs):
    """Format (key, value) pairs into a URL query string.

    The inverse of parse_qs: space encodes as '+', and '&', '=', '%', '+'
    plus every byte outside printable ASCII are percent-encoded as uppercase
    UTF-8 %XX pairs.
    """
    chunks = []
    for key, value in pairs:
        encoded_key = _encode_segment(key)
        encoded_value = _encode_segment(value)
        chunks.append(encoded_key + "=" + encoded_value)
    return "&".join(chunks)


def _encode_segment(text):
    out = []
    for byte in text.encode("utf-8"):
        if byte == 0x20:
            out.append("+")
        elif 0x21 <= byte <= 0x7E and chr(byte) not in _ALWAYS_ESCAPED:
            out.append(chr(byte))
        else:
            out.append("%" + format(byte, "02X"))
    return "".join(out)
