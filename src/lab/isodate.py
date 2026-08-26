def _is_leap_year(year):
    """Return True for a Gregorian leap year, False otherwise."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _validate(year, month, day):
    """Return None after confirming (year, month, day) is a legal Gregorian date.

    Raises ValueError when the month is not 1..12 or the day is illegal for
    the month and year.
    """
    if not 1 <= month <= 12:
        raise ValueError(f"month must be in 1..12, got {month}")
    days_per_month = [
        31,
        29 if _is_leap_year(year) else 28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    ]
    max_day = days_per_month[month - 1]
    if not 1 <= day <= max_day:
        raise ValueError(f"day must be in 1..{max_day} for {year}-{month:02d}, got {day}")


def _days_before_month(month):
    """Return the number of days in preceding months before the given month (1-indexed)."""
    return [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334][month - 1]


def day_of_year(year, month, day) -> int:
    """Return the day number within the year: Jan 1 is day 1.

    Raises ValueError on an illegal date.
    """
    _validate(year, month, day)
    ordinal = _days_before_month(month) + day
    if _is_leap_year(year) and month > 2:
        ordinal += 1
    return ordinal


def _monday_weekday(year, month, day):
    """Return the 1-based weekday (Monday=1 .. Sunday=7) for a validated date.

    1 Jan 0001 was a Monday, so the weekday is the day count mod 7, using the
    sum of days in all preceding years.
    """
    ordinal = day_of_year(year, month, day)
    for y in range(1, year):
        ordinal += 366 if _is_leap_year(y) else 365
    return (ordinal - 1) % 7 + 1


def iso_week(year, month, day):
    """Return the ISO 8601 week date as (iso_year, iso_week, iso_weekday).

    Weeks start on Monday (weekday 1). Week 1 is the week containing the
    year's first Thursday, so early January can fall in the previous ISO
    year and late December in the next. Raises ValueError on an illegal date.
    """
    _validate(year, month, day)
    weekday = _monday_weekday(year, month, day)

    # The day-of-year of the Thursday of the current week. The ISO year is the
    # year of that Thursday; the week number is its own week's ordinal.
    ordinal = day_of_year(year, month, day)
    thursday = ordinal + (4 - weekday)
    days_in_year = 366 if _is_leap_year(year) else 365

    if thursday > days_in_year:
        # The date falls in week 1 of the following ISO year.
        thursday -= days_in_year
        iso_year = year + 1
    elif thursday < 1:
        # The date falls in the last week of the previous ISO year.
        iso_year = year - 1
        days_prev = 366 if _is_leap_year(iso_year) else 365
        thursday += days_prev
    else:
        iso_year = year

    iso_week_number = (thursday - 1) // 7 + 1
    return iso_year, iso_week_number, weekday
