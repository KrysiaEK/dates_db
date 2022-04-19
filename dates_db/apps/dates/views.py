from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from dates_db.apps.dates.exceptions import NoDateError
from dates_db.apps.dates.models import Date
from dates_db.apps.dates.serializers import DateSerializer
from dates_db.apps.dates.utilities import Months, connect


class DateViewSet(viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet, viewsets.mixins.DestroyModelMixin):
    """Views set of ``Date`` model."""

    serializer_class = DateSerializer
    queryset = Date.objects.all()

    def create(self, request, *args, **kwargs):
        """Send request to numbersapi.com and save data in database."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data['month'] in [4, 6, 9, 11] and request.data['day'] == 31:
            raise NoDateError()
        elif request.data['month'] == 2 and request.data['day'] > 29:
            raise NoDateError()
        month = serializer.validated_data['month']
        day = serializer.validated_data['day']
        fact = connect(month, day)
        serializer.validated_data['fact'] = fact
        date = serializer.save()
        serializer = DateSerializer(date)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """List all dates in database."""

        dates = Date.objects.all()
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

    serializer_class = DateSerializer
    queryset = Date.objects.all()

    def list(self, request, *args, **kwargs):
        """List of months with the number of their checked days."""

        days_checked = Date.objects.values('month').annotate(days_checked=Count('day'))
        for element in days_checked:
            if element['month'] in dict(Months.Choices):
                element['id'] = element['month']
                element['month'] = Months.Choices[element['month']-1][1]
        return Response(days_checked, status=status.HTTP_200_OK)
