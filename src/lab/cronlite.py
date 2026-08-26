def _to_int(text, name):
    try:
        return int(text)
    except ValueError:
        raise ValueError(f"malformed {name} spec") from None


def _get_plain_values(spec, upper, name):
    values = set()
    for part in spec.split(","):
        if part == "" or any(ch in part for ch in "*/-"):
            raise ValueError(f"malformed {name} spec")
        value = _to_int(part, name)
        if value < 0 or value > upper:
            raise ValueError(f"{name} value out of range")
        values.add(value)
    if not values:
        raise ValueError(f"empty {name} spec")
    return values


def _parse_field(spec, upper, name):
    if spec is None or spec == "":
        raise ValueError(f"empty {name} spec")

    if spec == "*":
        return set(range(upper + 1))

    if spec.startswith("*/"):
        step = _to_int(spec[2:], name)
        if step == 0:
            raise ValueError(f"zero step in {name} spec")
        if step < 0:
            raise ValueError(f"negative step in {name} spec")
        values = set(range(0, upper + 1, step))
        if not values:
            raise ValueError(f"empty {name} spec")
        return values

    if "/" in spec:
        raise ValueError(f"malformed {name} spec")

    if "-" in spec:
        a_text, _, b_text = spec.partition("-")
        if a_text == "" or b_text == "":
            raise ValueError(f"malformed {name} spec")
        a = _to_int(a_text, name)
        b = _to_int(b_text, name)
        if a > b:
            raise ValueError(f"range {name} a must be <= b")
        if a < 0 or b > upper:
            raise ValueError(f"range out of {name} bounds")
        return set(range(a, b + 1))

    return _get_plain_values(spec, upper, name)


def next_run(minute_spec, hour_spec, after):
    minutes = _parse_field(minute_spec, 59, "minute")
    hours = _parse_field(hour_spec, 23, "hour")

    hour, minute = after
    while True:
        minute += 1
        if minute > 59:
            minute = 0
            hour += 1
            if hour > 23:
                hour = 0
        if hour in hours and minute in minutes:
            return (hour, minute)
