"""
Module providing serializers for the currencies app.
This module defines serializers for converting Currency
and HistoryCurrencies model instances to and from JSON format,
as well as for validating and saving favorite currencies for users.
"""

from rest_framework import serializers
from currencies import models
from django.shortcuts import get_object_or_404
from user import models as user_models


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = "__all__"


class HistoryCurrenciesSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = models.HistoryCurrencies
        fields = "__all__"


class FavoriteCurrencySerializer(serializers.Serializer):
    currency_id = serializers.IntegerField()

    def validate_currency_id(self, value: int) -> int:
        """
        Validate the provided currency ID.

        Args:
            value (int): The currency ID to validate.

        Returns:
            int: The validated currency ID.

        Raises:
            Http404: If the Currency object does not exist.

        """
        get_object_or_404(models.Currency, pk=value)
        return value

    def save(self, user: user_models.User, **kwargs: dict) -> models.FavoriteCurrency:
        """
        Save the favorite currency for the user.

        Args:
            user (User): The user for whom the favorite currency is being saved.
            **kwargs: Additional keyword arguments.

        Returns:
            FavoriteCurrency: The created or retrieved FavoriteCurrency instance.

        """
        validated_data = self.validated_data
        currency_id = validated_data["currency_id"]

        currency = models.Currency.objects.get(pk=currency_id)
        favorite_currency = models.FavoriteCurrency.objects.get_or_create(
            currency=currency, user=user
        )
        return favorite_currency
