def greet() -> str:
    return "hello from the lab"


def count_words(text: str) -> int:
    return len(text.split())


def is_palindrome(text: str) -> bool:
    normalized = "".join(ch for ch in text.lower() if not ch.isspace())
    return normalized == normalized[::-1]
