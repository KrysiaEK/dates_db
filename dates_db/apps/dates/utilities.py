import coreapi


def connect(month, day):
    """Connect nubersapi API."""

    client = coreapi.Client()
    fact = client.get(f'http://numbersapi.com/{month}/{day}/date')
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
