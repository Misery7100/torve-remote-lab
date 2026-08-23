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
