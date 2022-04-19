from rest_framework import serializers

from dates_db.apps.dates.models import Date


class DateSerializer(serializers.ModelSerializer):
    """Serializer of ``Date`` model instances."""

    fact = serializers.CharField(read_only=True)

    class Meta:
        model = Date
        fields = ['id', 'month', 'day', 'fact']
