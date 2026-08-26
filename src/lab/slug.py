def slugify(text: str, max_len: int = 64) -> str:
    if max_len < 1:
        raise ValueError("max_len must be positive")

    fold = {
        "à": "a", "á": "a", "â": "a", "ã": "a", "ä": "a", "å": "a",
        "æ": "ae",
        "ç": "c",
        "è": "e", "é": "e", "ê": "e", "ë": "e",
        "ì": "i", "í": "i", "î": "i", "ï": "i",
        "ñ": "n",
        "ò": "o", "ó": "o", "ô": "o", "õ": "o", "ö": "o",
        "ø": "o",
        "ù": "u", "ú": "u", "û": "u", "ü": "u",
        "ý": "y",
        "ß": "ss",
    }

    mapped = "".join(fold.get(ch, ch) for ch in text.lower())

    chars = []
    for ch in mapped:
        is_word_char = ("a" <= ch <= "z") or ("0" <= ch <= "9")
        if not is_word_char:
            if chars and chars[-1] != "-":
                chars.append("-")
        else:
            chars.append(ch)
    slug = "".join(chars).strip("-")

    if len(slug) <= max_len:
        return slug

    cut = slug.rfind("-", 0, max_len + 1)
    if cut <= 0:
        return slug[:max_len]
    return slug[:cut]
