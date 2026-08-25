def parse_csv(text: str) -> list:
    """Parse RFC 4180-style CSV text into a list of rows, each a list of fields.

    Fields are separated by commas. Fields containing a comma, double quote, or
    newline are quoted with double quotes, and an embedded double quote is
    escaped by doubling it. Accepts LF and CRLF line endings, preserves empty
    fields, and treats a trailing newline as row termination rather than an
    extra empty row.

    Raises ValueError on an unterminated quoted field or on characters after a
    closing quote that are not a comma or line end.
    """
    if not text:
        return []

    rows = []
    field_chars = []
    row_fields = []
    in_quotes = False

    def finish_field():
        row_fields.append("".join(field_chars))
        field_chars[:] = []

    def finish_row():
        finish_field()
        rows.append(list(row_fields))
        row_fields[:] = []

    index = 0
    length = len(text)

    while index < length:
        char = text[index]

        if in_quotes:
            if char == '"':
                if index + 1 < length and text[index + 1] == '"':
                    field_chars.append('"')
                    index += 2
                    continue
                in_quotes = False
                index += 1
                if index >= length:
                    break
                next_char = text[index]
                if next_char == ",":
                    finish_field()
                    index += 1
                    continue
                if next_char == "\r":
                    if index + 1 < length and text[index + 1] == "\n":
                        index += 2
                    else:
                        index += 1
                    finish_row()
                    continue
                if next_char == "\n":
                    index += 1
                    finish_row()
                    continue
                raise ValueError(
                    "character after closing quote must be a comma or line end"
                )
            if char == "\r":
                field_chars.append("\r")
                index += 1
                continue
            field_chars.append(char)
            index += 1
            continue

        if char == '"':
            if not field_chars:
                in_quotes = True
                index += 1
                continue
            raise ValueError("unexpected double quote in unquoted field")

        if char == ",":
            finish_field()
            index += 1
            continue

        if char == "\r":
            if index + 1 < length and text[index + 1] == "\n":
                index += 2
            else:
                index += 1
            finish_row()
            continue

        if char == "\n":
            index += 1
            finish_row()
            continue

        field_chars.append(char)
        index += 1

    if in_quotes:
        raise ValueError("unterminated quoted field")

    if field_chars or row_fields:
        finish_row()

    return rows


def render_csv(rows: list) -> str:
    """Render rows of string fields as RFC 4180-style CSV text.

    Quotes a field only when it contains a comma, double quote, or newline.
    Round-trips with parse_csv: parse_csv(render_csv(rows)) == rows.
    """
    rendered_rows = []
    for row in rows:
        rendered_fields = []
        for field in row:
            field = str(field)
            if any(ch in field for ch in ',"\r\n'):
                field = '"' + field.replace('"', '""') + '"'
            rendered_fields.append(field)
        rendered_rows.append(",".join(rendered_fields))
    return "\n".join(rendered_rows)
