from rest_framework import serializers
from currencies import models


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = "__all__"


class HistoryCurrenciesSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = models.HistoryCurrencies
        fields = "__all__"
