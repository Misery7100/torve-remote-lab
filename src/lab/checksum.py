_TABLE = (
    (0, 3, 1, 7, 5, 9, 8, 6, 4, 2),
    (7, 0, 9, 2, 1, 5, 4, 8, 6, 3),
    (4, 2, 0, 6, 8, 7, 1, 3, 5, 9),
    (1, 7, 5, 0, 9, 8, 3, 4, 2, 6),
    (6, 1, 2, 3, 0, 4, 5, 9, 7, 8),
    (3, 6, 7, 4, 2, 0, 9, 5, 8, 1),
    (5, 8, 6, 9, 7, 2, 0, 1, 3, 4),
    (8, 9, 4, 5, 3, 6, 2, 0, 1, 7),
    (9, 4, 3, 8, 6, 1, 7, 2, 0, 5),
    (2, 5, 8, 1, 4, 3, 6, 7, 9, 0),
)

_LUHN_TABLE = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)


def _require_digits(digits: str) -> None:
    if not all(ch.isdigit() for ch in digits):
        raise ValueError("digits must contain only digit characters")


def luhn_valid(digits: str) -> bool:
    """Return True when the digit string passes the Luhn checksum, False otherwise.

    Raises ValueError when the input contains non-digit characters.
    """
    _require_digits(digits)
    total = 0
    for index, ch in enumerate(digits):
        value = int(ch)
        if (len(digits) - index) % 2 == 0:
            value = _LUHN_TABLE[value]
        total += value
    return total % 10 == 0


def compute_damm_check_digit(digits: str) -> str:
    """Return the Damm check digit to append so the full string validates.

    Raises ValueError when the input contains non-digit characters.
    """
    _require_digits(digits)
    interim = 0
    for ch in digits:
        interim = _TABLE[interim][int(ch)]
    return str(interim)


def damm_valid(digits: str) -> bool:
    """Return True when the digit string (including its check digit) passes the Damm checksum.

    Raises ValueError when the input contains non-digit characters.
    """
    _require_digits(digits)
    interim = 0
    for ch in digits:
        interim = _TABLE[interim][int(ch)]
    return interim == 0
