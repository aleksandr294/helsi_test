import typing

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from currencies import models as currencies_models
from django.utils import timezone
import datetime


DATE_TEMPLATE: str = "%Y-%m-%dT%H:%M:%S.%fZ"
DATE: datetime.datetime = datetime.datetime(
    year=2024, month=5, day=1, tzinfo=datetime.timezone.utc
)
MINUTE: int = 30


class TestCurrencies(TestCase):
    def setUp(self):
        self.client = APIClient()

    def create_currencies(self) -> typing.Tuple[currencies_models.Currency]:
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
        currencies,
        currenct_time: datetime.datetime,
        actualy_end: datetime.datetime,
    ):

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

    def test_get_current_currencies_list(self):
        currenct_time = timezone.now()
        currenct_time_str = currenct_time.strftime(DATE_TEMPLATE)

        actualy_end = currenct_time + datetime.timedelta(minutes=MINUTE)
        actualy_end_str = actualy_end.strftime(DATE_TEMPLATE)

        mock_currencies = self.create_currencies()
        self.create_history_currencies(
            currencies=mock_currencies,
            currenct_time=currenct_time,
            actualy_end=actualy_end,
        )

        url = reverse("current")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            dict(
                id=1,
                currency=dict(id=1, code=1, text_code="TS1", name="TEST1"),
                rate="1.00000",
                date=currenct_time_str,
                actualy_end=actualy_end_str,
            ),
            dict(
                id=2,
                currency=dict(id=2, code=2, text_code="TS2", name="TEST2"),
                rate="2.00000",
                date=currenct_time_str,
                actualy_end=actualy_end_str,
            ),
        ]
        resutls = list(response.data["results"])
        self.assertEqual(resutls, expected_data)
