from rest_framework import status, viewsets
from rest_framework.response import Response

from dates_db.apps.dates.exceptions import NoDateError
from dates_db.apps.dates.models import Date
from dates_db.apps.dates.serializers import DateSerializer
from dates_db.apps.dates.utilities import connect


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
