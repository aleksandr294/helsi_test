"""
Module contains unit tests for
currency-related APIs in the Django application.
It includes tests for retrieving current and historical
currency data, creating and deleting favorite currencies,
as well as validating the behavior with different filters and input data.
"""

import typing

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from currencies import models as currencies_models
from django.utils import timezone
import datetime
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


DATE: datetime.datetime = datetime.datetime(
    year=2024, month=5, day=1, tzinfo=datetime.timezone.utc
)
MINUTE: int = 30


class TestCurrencies(TestCase):
    def setUp(self):
        """Set up initial data and authenticate a user for testing."""
        self.client = APIClient()

        self.currenct_time = timezone.now()
        self.actualy_end = self.currenct_time + timezone.timedelta(minutes=MINUTE)

        self.user = get_user_model().objects.create_user(
            email="test@mail.com", password="test"  # noqa: S106
        )

        self.mock_currencies = self.create_currencies()
        self.create_history_currencies(
            currencies=self.mock_currencies,
            currenct_time=self.currenct_time,
            actualy_end=self.actualy_end,
        )
        self.favorite_currency = self.create_favorite_currencies(
            currencies=self.mock_currencies, user=self.user
        )

        self.token = RefreshToken.for_user(self.user)
        self.client.force_authenticate(user=self.user, token=self.token.access_token)

    def create_currencies(self) -> typing.Tuple[typing.Any, typing.Any, typing.Any]:
        """
        Create mock currency objects for testing.

        Returns:
            Tuple[currencies_models.Currency]: A tuple of created currency objects.

        """
        mock_currency_1 = currencies_models.Currency.objects.create(
            code=1, text_code="TS1", name="TEST1"
        )
        mock_currency_2 = currencies_models.Currency.objects.create(
            code=2, text_code="TS2", name="TEST2"
        )
        mock_currency_3 = currencies_models.Currency.objects.create(
            code=3, text_code="TS3", name="TEST3"
        )

        return mock_currency_1, mock_currency_2, mock_currency_3

    def create_history_currencies(
        self,
        currencies: typing.List[currencies_models.Currency],
        currenct_time: datetime.datetime,
        actualy_end: datetime.datetime,
    ):
        """
        Create mock history currency objects for testing.

        Args:
            currencies: A tuple of currency objects.
            currenct_time (datetime.datetime): Current datetime.
            actualy_end (datetime.datetime): Datetime indicating the actual end time.

        Returns:
            None

        """

        currencies_models.HistoryCurrencies.objects.create(
            currency=currencies[0],
            rate=1.0,
            date=currenct_time,
            actualy_end=actualy_end,
        )
        currencies_models.HistoryCurrencies.objects.create(
            currency=currencies[1],
            rate=2.0,
            date=currenct_time,
            actualy_end=actualy_end,
        )

        currencies_models.HistoryCurrencies.objects.create(
            currency=currencies[2],
            rate=2.0,
            date=DATE,
            actualy_end=DATE + datetime.timedelta(minutes=MINUTE),
        )

    def create_favorite_currencies(
        self,
        currencies: typing.List[currencies_models.Currency],
        user,
    ) -> currencies_models.FavoriteCurrency:
        """
        Create mock favorite currency objects for testing.

        Args:
            currencies (List[currencies_models.Currency]): List of currency objects.
            user: User object.

        Returns:
            currencies_models.FavoriteCurrency: Created favorite currency object.

        """
        currencies_favorite = currencies_models.FavoriteCurrency.objects.create(
            currency=currencies[0], user=user
        )
        return currencies_favorite

    def test_01_get_current_currencies_list(self):
        """Test to get the list of current currencies."""
        url = reverse("current")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data["results"]
        self.assertEqual(len(data), 2)

    def test_02_get_currencies_list(self):
        """Test to get the list of all currencies."""

        url = reverse("currencies")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data["results"]

        self.assertEqual(len(data), 3)

    def test_03_get_history_currencies(self):
        """Test retrieving historical currency data without filters."""
        url = reverse("history")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data["results"]
        self.assertEqual(len(data), 3)

    def test_04_get_history_currencies_with_date_filter(self):
        """Test retrieving historical currency data with date range filter."""
        url = reverse("history")
        date_from = (timezone.now() - timezone.timedelta(days=1)).isoformat()
        date_to = (timezone.now() + timezone.timedelta(minutes=MINUTE)).isoformat()

        response = self.client.get(url, dict(date_from=date_from, date_to=date_to))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data["results"]
        self.assertEqual(len(data), 2)

    def test_05_get_history_currencies_with_currency_id_filter(self):
        """Test retrieving historical currency data filtered by currency ID."""
        url = reverse("history")
        response = self.client.get(url, dict(currency_id=self.mock_currencies[0].pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data["results"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["currency"]["id"], self.mock_currencies[0].pk)

    def test_06_create_favorite_currency(self):
        """Test creating a favorite currency for the authenticated user."""
        url = reverse("create_favorite")
        data = dict(currency_id=self.mock_currencies[0].pk)

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_07_create_favorite_currency_invalid_data(self):
        """Test creating a favorite currency with invalid data."""
        url = reverse("create_favorite")
        data = dict()

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_08_delete_favorite_currency(self):
        """Test deleting a favorite currency."""
        url = reverse(
            "delete_favorite",
            kwargs=dict(currency_id=self.favorite_currency.currency.pk),
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_09_delete_favorite_currency_invalid_currency_id(self):
        """Test deleting a favorite currency with an invalid currency ID."""
        url = reverse("delete_favorite", kwargs=dict(currency_id=999))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
