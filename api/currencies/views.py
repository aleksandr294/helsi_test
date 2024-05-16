from rest_framework import generics
from currencies import serializers as currencies_serializer, models as currencies_models
import datetime


class CurrentCurrenciesListAPIView(generics.ListAPIView):
    """Returns a list of current currencies."""

    serializer_class = currencies_serializer.CurrenciesSerializer

    def get_queryset(self):
        """
         Retrieves and returns a queryset of currencies valid for the current date.

        Returns:
            QuerySet: A query to the Currencies model, filtered by the current date.

        """
        current_date = datetime.datetime.utcnow().date()
        queryset = currencies_models.Сurrencies.objects.filter(date=current_date)
        return queryset
