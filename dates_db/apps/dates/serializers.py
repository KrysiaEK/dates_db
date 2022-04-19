from rest_framework import serializers

from dates_db.apps.dates.models import Date
from dates_db.apps.dates.utilities import Months


class DateSerializer(serializers.ModelSerializer):
    """Serializer of ``Date`` model instances."""

    month = serializers.ChoiceField(choices=Months.Choices, source='get_month_display')
    fact = serializers.CharField(read_only=True)

    class Meta:
        model = Date
        fields = ['id', 'month', 'day', 'fact']
