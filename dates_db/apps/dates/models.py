from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from dates_db.apps.dates.utilities import Months


class Date(models.Model):
    """Model representing date."""

    month = models.PositiveSmallIntegerField(choices=Months.Choices)
    day = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    fact = models.TextField()

    class Meta:
        verbose_name = 'Date'
        verbose_name_plural = 'Dates'
