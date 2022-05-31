import coreapi
from coreapi.exceptions import CoreAPIException

from dates_db.apps.dates.exceptions import NoDateError, InvalidFactError


def validate_month_and_day(month, day):
    if month <= 0 or month > 12:
        raise NoDateError()
    if day <= 0 or day > 31:
        raise NoDateError()
    if month in [4, 6, 9, 11] and day == 31:
        raise NoDateError()
    elif month == 2 and day > 29:
        raise NoDateError()


def get_fact(month, day):
    """Get fact from nubersapi API."""

    client = coreapi.Client()
    try:
        fact = client.get(f'http://numbersapi.com/{month}/{day}/date')
    except CoreAPIException:
        raise InvalidFactError()
    if not isinstance(fact, str):
        raise InvalidFactError()
    return fact


class Months:
    """Months choices."""

    Choices = (
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    )
