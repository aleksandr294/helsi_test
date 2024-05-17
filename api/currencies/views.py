from django.utils import timezone
from rest_framework import generics
from currencies import (
    serializers as currencies_serializer,
    models as currencies_models,
    filters as currencies_filters,
)
from django_filters import rest_framework as filters


class CurrentCurrenciesListAPIView(generics.ListAPIView):
    """Returns a list of current currencies."""

    serializer_class = currencies_serializer.HistoryCurrenciesSerializer

    def get_queryset(self):
        """
         Retrieves and returns a queryset of currencies valid for the current time.

        Returns:
            QuerySet: A query to the Currencies model, filtered by the current time.

        """
        current_time = timezone.now()
        queryset = currencies_models.HistoryCurrencies.objects.filter(
            date__lt=current_time, actualy_end__gt=current_time
        )

        return queryset


class CurrenciesListAPIView(generics.ListAPIView):

    serializer_class = currencies_serializer.CurrencySerializer
    queryset = currencies_models.Currency.objects.all()


class HistoryCurrenciesListAPIView(generics.ListAPIView):

    serializer_class = currencies_serializer.HistoryCurrenciesSerializer
    queryset = currencies_models.HistoryCurrencies.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = currencies_filters.DateTimeRangeFilter
