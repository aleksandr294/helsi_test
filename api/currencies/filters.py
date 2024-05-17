"""
Module providing a custom Django FilterSet
for filtering currency history data.
This module defines a custom Django FilterSet class,
`DateTimeRangeFilter`,
which is used to filter currency history data based
on date range and currency ID.
"""

from django_filters import rest_framework as filters
from currencies import models as currencies_models


class DateTimeRangeFilter(filters.FilterSet):
    date_from = filters.DateTimeFilter(field_name="date", lookup_expr="gte")
    date_to = filters.DateTimeFilter(field_name="date", lookup_expr="lte")
    currency_id = filters.CharFilter(field_name="currency", lookup_expr="exact")

    class Meta:
        model = currencies_models.HistoryCurrencies
        fields = ["date_from", "date_to", "currency_id"]  # noqa: RUF012
