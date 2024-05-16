from rest_framework import serializers
from currencies import models


class CurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Сurrencies
        fields = "__all__"
