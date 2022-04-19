from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey

from dates_db.apps.dates.models import Date
from dates_db.apps.dates.tests.factories import DateFactory


class DateApiTestCase(APITestCase):
    """Tests of ``Date`` views methods."""

    @classmethod
    def setUpClass(cls):
        """Setup related models, key, url required to run tests."""
        super().setUpClass()
        cls.api_key, cls.key = APIKey.objects.create_key(name="X-API-KEY")
        cls.dates_url = '/dates/'
        cls.date1 = DateFactory(
            month=3,
            day=2,
            fact="March 2nd is the day in 986 that Louis V becomes King of the Franks."
        )
        cls.date2 = DateFactory(
            month=4,
            day=4,
            fact="April 4th is the day in 1850 that Los Angeles, California is incorporated as a city."
        )
        cls.date3 = DateFactory(
            month=5,
            day=5,
            fact="May 5th is the day in 1964 that the Council of Europe declares May 5 as Europe Day."
        )
        cls.date4 = DateFactory(
            month=4,
            day=4,
            fact="April 4th is the day in 1979 that the 2nd Congress of the Communist Youth of Greece starts."
        )

    @patch('dates_db.apps.dates.views.connect')
    def test_get_and_create_date(self, mock_response):
        """Ensure date is properly created."""

        mock_response.return_value = "June 6th is the day in 2002 that Eastern Mediterranean Event."
        response = self.client.post(
            path=self.dates_url,
            data={
                'month': 6,
                'day': 6,
            },
            format='json',
        )
        self.assertTrue(
            Date.objects.filter(
                month=6,
                day=6,
                fact="June 6th is the day in 2002 that Eastern Mediterranean Event."
            ).exists()
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_not_date(self):
        """Ensure http 400 is returned when day > 31 or month > 12."""

        response = self.client.post(
            path=self.dates_url,
            data={
                'month': 16,
                'day': 6,
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wrong_date(self):
        """Ensure http 400 is returned when month is shorter than requested."""

        response = self.client.post(
            path=self.dates_url,
            data={
                'month': 2,
                'day': 30,
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('detail'), "No such date.")

    def test_dates_list(self):
        """Ensure list of dates is properly returned."""

        response = self.client.get(
            path=self.dates_url,
            format='json',
        )
        self.assertEqual(
            [element['id'] for element in response.json()],
            [self.date1.id, self.date2.id, self.date3.id, self.date4.id]
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_with_apikey(self):
        """Ensure date is deleted when good api key is given."""

        headers = {"HTTP_X_API_KEY": self.key}
        response = self.client.delete(
            path='/dates/1/',
            format='json',
            **headers
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_not_deleted_with_wrong_apikey(self):
        """Ensure http 403 is raised and date not deleted when wrong key is given."""

        headers = {"HTTP_X_API_KEY": "wrong_key"}
        response = self.client.delete(
            path='/dates/1/',
            format='json',
            **headers
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json().get('detail'), 'Authentication credentials were not provided.')
        self.assertTrue(Date.objects.filter(id=1).exists())

    def test_delete_no_apikey(self):
        """Ensure http 403 is raised and date not deleted when key is not given."""

        response = self.client.delete(
            path='/dates/1/',
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json().get('detail'), 'Authentication credentials were not provided.')
        self.assertTrue(Date.objects.filter(id=1).exists())

    def test_delete_object_not_exists(self):
        """Ensure http 404 is raised when date doesn't exist in database."""

        headers = {"HTTP_X_API_KEY": self.key}
        response = self.client.delete(
            path='/dates/5/',
            format='json',
            **headers
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json().get('detail'), 'Not found.')


class PopularityApiTestCase(APITestCase):
    """Tests of ``Popularity`` views methods."""

    @classmethod
    def setUpClass(cls):
        """Setup related models, url required to run tests."""
        super().setUpClass()
        cls.dates_url = '/popular/'
        cls.date1 = DateFactory(
            month=3,
            day=2,
            fact="March 2nd is the day in 986 that Louis V becomes King of the Franks."
        )
        cls.date2 = DateFactory(
            month=4,
            day=4,
            fact="April 4th is the day in 1850 that Los Angeles, California is incorporated as a city."
        )
        cls.date3 = DateFactory(
            month=5,
            day=5,
            fact="May 5th is the day in 1964 that the Council of Europe declares May 5 as Europe Day."
        )
        cls.date4 = DateFactory(
            month=4,
            day=4,
            fact="April 4th is the day in 1979 that the 2nd Congress of the Communist Youth of Greece starts."
        )

    def test_popularity_list(self):
        """Ensure month popularity statistics are properly returned."""

        response = self.client.get(
            path='/popular/',
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), [
                {'month': 'March', 'days_checked': 1, 'id': 3},
                {'month': 'May', 'days_checked': 1, 'id': 5},
                {'month': 'April', 'days_checked': 2, 'id': 4}
            ]
        )
