from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import datetime
from currencies import models as currencies_models


class TestCurrencies(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_current_currencies_list(self):
        current_date = datetime.datetime.utcnow().date()
        current_date_str = current_date.strftime("%Y-%m-%d")

        currencies_models.Сurrencies.objects.create(
            code=1,
            text_code="T1",
            rate=1.0,
            date=current_date,
        )
        currencies_models.Сurrencies.objects.create(
            code=2,
            text_code="T2",
            rate=2.0,
            date=current_date,
        )
        currencies_models.Сurrencies.objects.create(
            code=3,
            text_code="T3",
            rate=2.0,
            date=datetime.datetime(day=1, month=2, year=2024),
        )

        url = reverse("current")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        queryset = currencies_models.Сurrencies.objects.filter(date=current_date)
        expected_data = [
            dict(
                id=1,
                code=1,
                text_code="T1",
                rate="1.00000",
                date=current_date_str,
            ),
            dict(
                id=2,
                code=2,
                text_code="T2",
                rate="2.00000",
                date=current_date_str,
            ),
        ]
        resutls = list(response.data["results"])
        self.assertEqual(resutls, expected_data)
