from django.db.models import Count, F
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from dates_db.apps.dates.exceptions import NoDateError
from dates_db.apps.dates.models import Date
from dates_db.apps.dates.serializers import DateSerializer
from dates_db.apps.dates.utilities import (Months, get_fact,
                                           validate_month_and_day)


class DateViewSet(viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet, viewsets.mixins.DestroyModelMixin):
    """Views set of ``Date`` model."""

    serializer_class = DateSerializer
    queryset = Date.objects.all()

    def create(self, request, *args, **kwargs):
        """Send request to numbersapi.com and save data in database."""

        try:
            month = int(request.data['month'])
            day = int(request.data['day'])
        except ValueError:
            raise NoDateError()
        validate_month_and_day(month, day)
        fact = get_fact(month, day)
        date = self.get_queryset().create(day=day, month=month, fact=fact)
        serializer = self.get_serializer(date)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """List all dates in database."""

        dates = self.get_queryset().all()
        serializer = self.get_serializer(dates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        """Set Api Key permission on method delete."""

        method = self.request.method
        if method == 'DELETE':
            return [HasAPIKey()]
        else:
            return []


class PopularityViewSet(viewsets.GenericViewSet):
    """Views set of ``Date`` model with popularity check."""

    queryset = Date.objects.all()

    def list(self, request, *args, **kwargs):
        """List of months with the number of their checked days."""

        days_checked = self.get_queryset().values('month').annotate(days_checked=Count('day')).annotate(id=F('month'))
        months = dict(Months.Choices)
        for element in days_checked:
            if element['month'] in months:
                element['month'] = months[element['month']]
        return Response(days_checked, status=status.HTTP_200_OK)
