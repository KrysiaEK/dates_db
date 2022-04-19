import factory

from dates_db.apps.dates.models import Date


class DateFactory(factory.django.DjangoModelFactory):
    """Factory of ``Date`` model instances."""

    class Meta:
        model = Date
