def running_total(numbers: list) -> list:
    """Return the list of cumulative sums; empty list for empty input."""
    totals = []
    running = 0
    for number in numbers:
        running += number
        totals.append(running)
    return totals


def greet() -> str:
    return "hello from the lab"


def count_words(text: str) -> int:
    return len(text.split())


def reverse_words(text: str) -> str:
    return " ".join(reversed(text.split()))


def is_palindrome(text: str) -> bool:
    normalized = "".join(ch for ch in text.lower() if ch != " ")
    return normalized == normalized[::-1]


def word_lengths(text: str) -> list:
    return [len(word) for word in text.split()]


def longest_word(text: str) -> str:
    return max(text.split(), key=len) if text.split() else ""


def vowel_count(text: str) -> int:
    """Count vowels — an operator hotfix landing mid-flight."""
    return sum(1 for ch in text.lower() if ch in "aeiou")


def digit_count(text: str) -> int:
    """Count digits — a second operator hotfix, landing under T-0026."""
    return sum(1 for ch in text if ch.isdigit())


def most_common_word(text: str) -> str:
    """Return the most frequent word, lower-cased; ties go to first appearance."""
    words = text.split()
    if not words:
        return ""
    counts = {}
    first = {}
    for index, word in enumerate(words):
        lowered = word.lower()
        counts[lowered] = counts.get(lowered, 0) + 1
        first.setdefault(lowered, index)
    return max(counts, key=lambda w: (counts[w], -first[w]))


def char_count(text: str) -> int:
    return sum(1 for ch in text if not ch.isspace())


def initials(text: str) -> str:
    return "".join(word[0].upper() for word in text.split())


def is_pangram(text: str) -> bool:
    """Return True when text uses every letter of the English alphabet at least once."""
    present = set(ch for ch in text.lower() if ch.isalpha())
    return present >= set("abcdefghijklmnopqrstuvwxyz")


def remove_punctuation(text: str) -> str:
    """Return text with all ASCII punctuation characters removed."""
    import string

    return "".join(ch for ch in text if ch not in string.punctuation)


def caesar_cipher(text: str, shift: int) -> str:
    """Rotate ASCII letters by shift, preserving case and leaving others untouched."""
    import string

    result = []
    for ch in text:
        if ch in string.ascii_lowercase:
            result.append(chr((ord(ch) - ord("a") + shift) % 26 + ord("a")))
        elif ch in string.ascii_uppercase:
            result.append(chr((ord(ch) - ord("A") + shift) % 26 + ord("A")))
        else:
            result.append(ch)
    return "".join(result)


def is_isogram(text: str) -> bool:
    """Return True when no letter repeats case-insensitively, ignoring non-letters."""
    seen = set()
    for ch in text.lower():
        if ch.isalpha():
            if ch in seen:
                return False
            seen.add(ch)
    return True


def anagrams(word: str, candidates: list) -> list:
    """Return candidates that are anagrams of word, case-insensitively.

    A word never counts as its own anagram.
    """
    target = sorted(word.lower())
    return [
        candidate
        for candidate in candidates
        if candidate.lower() != word.lower() and sorted(candidate.lower()) == target
    ]


def hamming_distance(a: str, b: str) -> int:
    """Return the number of differing positions between two equal-length strings."""
    if len(a) != len(b):
        raise ValueError("strings must be of equal length")
    return sum(1 for x, y in zip(a, b) if x != y)


def roman_numeral(n: int) -> str:
    """Return the Roman numeral string for integer n in the range 1..3999.

    Raises ValueError when n is not an integer or is outside that range.
    """
    if not isinstance(n, int) or not 1 <= n <= 3999:
        raise ValueError("n out of range 1..3999 for Roman numeral conversion")
    numerals = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]
    result = []
    for value, symbol in numerals:
        while n >= value:
            result.append(symbol)
            n -= value
    return "".join(result)


def from_roman(text: str) -> int:
    """Return the integer for a Roman numeral string in the range 1..3999.

    Raises ValueError when the string is not a valid canonical Roman numeral
    in that range.
    """
    if not isinstance(text, str):
        raise ValueError("input must be a string")
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    previous = 0
    for ch in text:
        if ch not in values:
            raise ValueError(f"invalid Roman numeral: {text!r}")
        value = values[ch]
        total += value
        if value > previous:
            total -= 2 * previous
        previous = value
    if not 1 <= total <= 3999 or roman_numeral(total) != text:
        raise ValueError(f"invalid Roman numeral: {text!r}")
    return total


def luhn_valid(digits: str) -> bool:
    """Return True when the digit string passes the Luhn checksum, False otherwise.

    Raises ValueError when the input contains non-digit characters.
    """
    if not all(ch.isdigit() for ch in digits):
        raise ValueError("digits must contain only digit characters")
    total = 0
    for index in range(len(digits) - 1, -1, -1):
        value = int(digits[index])
        if (len(digits) - index) % 2 == 0:
            value *= 2
            if value > 9:
                value -= 9
        total += value
    return total % 10 == 0


def balanced_brackets(text: str) -> bool:
    """Return True when every (), [], {} pair in the text nests and closes correctly, ignoring other characters."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in pairs.values():
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


def rle_encode(text: str) -> str:
    """Run-length encode a string as character-count pairs like a3b1; empty for empty input."""
    if not text:
        return ""
    result = []
    prev = text[0]
    count = 1
    for ch in text[1:]:
        if ch == prev:
            count += 1
        else:
            result.append(f"{prev}{count}")
            prev = ch
            count = 1
    result.append(f"{prev}{count}")
    return "".join(result)


def rle_decode(text: str) -> str:
    """Run-length decode a string of character-count pairs like a3b1 back to raw text.

    Returns an empty string for empty input. Raises ValueError when the text
    contains a malformed pair (a character not followed by a count).
    """
    if not text:
        return ""
    result = []
    index = 0
    while index < len(text):
        char = text[index]
        index += 1
        count_start = index
        while index < len(text) and text[index].isdigit():
            index += 1
        if count_start == index:
            raise ValueError(f"malformed run-length encoded text: {text!r}")
        result.append(char * int(text[count_start:index]))
    if not result:
        raise ValueError(f"malformed run-length encoded text: {text!r}")
    return "".join(result)


def collatz_steps(n: int) -> int:
    """Return the number of Collatz steps required to reach 1 from positive integer n.

    Raises ValueError if n is not a positive integer.
    """
    if n < 1:
        raise ValueError("n must be a positive integer")
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps


def levenshtein(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between two strings.

    Insertions, deletions, and substitutions each cost 1. Implemented
    iteratively using O(min(len(a), len(b))) additional space. The function
    is symmetric and accepts empty strings (distance is the other's length).
    """
    if len(a) < len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i, ch_a in enumerate(a, 1):
        current = [i]
        for j in range(1, len(b) + 1):
            cost = 0 if ch_a == b[j - 1] else 1
            current.append(
                min(
                    current[-1] + 1,
                    previous[j] + 1,
                    previous[j - 1] + cost,
                )
            )
        previous = current
    return previous[-1]
