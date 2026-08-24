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
