"""
Module defines views for currency-related
APIs in the Django application.
It includes views to list current currencies,
all available currencies, historical currency data,
create and delete favorite currencies, and list
current favorite currencies for authenticated users.
"""

from django.utils import timezone
from rest_framework import generics, response, status, request
from currencies import (
    serializers as currencies_serializer,
    models as currencies_models,
    filters as currencies_filters,
)
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


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
    """View to list all available currencies."""

    serializer_class = currencies_serializer.CurrencySerializer
    queryset = currencies_models.Currency.objects.all()


class HistoryCurrenciesListAPIView(generics.ListAPIView):
    """View to list historical data of currencies within a specified date range."""

    serializer_class = currencies_serializer.HistoryCurrenciesSerializer
    queryset = currencies_models.HistoryCurrencies.objects.all()
    filter_backends = [filters.DjangoFilterBackend]  # noqa: RUF012
    filterset_class = currencies_filters.DateTimeRangeFilter


class CreateFavoriteCurrencyAPIView(generics.CreateAPIView):
    """View to create a favorite currency for the authenticated user."""

    serializer_class = currencies_serializer.FavoriteCurrencySerializer
    queryset = currencies_models.HistoryCurrencies.objects.all()
    permission_classes = [IsAuthenticated]  # noqa: RUF012

    def create(self, request: request.Request, *args: tuple, **kwargs: dict):
        """Create a favorite currency for the authenticated user."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return response.Response(status=status.HTTP_201_CREATED)


class DeleteFavoriteCurrencyAPIView(generics.DestroyAPIView):
    """View to delete a favorite currency for the authenticated user."""

    queryset = currencies_models.HistoryCurrencies.objects.all()
    permission_classes = [IsAuthenticated]  # noqa: RUF012

    def delete(self, request: request.Request, *args: tuple, **kwargs: dict):
        """Delete a favorite currency for the authenticated user."""

        currency_id = self.kwargs["currency_id"]
        currency = get_object_or_404(currencies_models.Currency, pk=currency_id)

        favorite_currency = get_object_or_404(
            currencies_models.FavoriteCurrency, currency=currency, user=request.user
        )
        favorite_currency.delete()

        return response.Response(status=status.HTTP_204_NO_CONTENT)


class CurrentFavoriteCurrenciesListAPIView(generics.ListAPIView):
    """View to list current favorite currencies for the authenticated user."""

    serializer_class = currencies_serializer.HistoryCurrenciesSerializer
    permission_classes = [IsAuthenticated]  # noqa: RUF012

    def get_queryset(self):
        """Get queryset of current favorite currencies for the authenticated user."""
        current_time = timezone.now()

        favorite_currencies = currencies_models.FavoriteCurrency.objects.filter(
            user=self.request.user
        ).select_related("currency")

        queryset = currencies_models.HistoryCurrencies.objects.filter(
            currency__in=favorite_currencies.values_list("currency", flat=True),
            date__lt=current_time,
            actualy_end__gt=current_time,
        )

        return queryset
