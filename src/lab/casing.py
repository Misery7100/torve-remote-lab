def snake_case(text: str) -> str:
    return "_".join(word.lower() for word in text.split())
