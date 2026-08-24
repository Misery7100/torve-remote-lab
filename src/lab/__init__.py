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


def is_isogram(text: str) -> bool:
    """Return True when no letter repeats case-insensitively, ignoring non-letters."""
    seen = set()
    for ch in text:
        if ch.isalpha():
            lowered = ch.lower()
            if lowered in seen:
                return False
            seen.add(lowered)
    return True
