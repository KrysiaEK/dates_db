from rest_framework import exceptions, status


class NoDateError(exceptions.APIException):
    """Ensure http 400 is returned, when date doesn't exist in life."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'No such date.'
