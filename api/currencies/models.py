"""
Module defining the models for the currencies app.
This module contains the model definitions for the currencies app,
including models for currencies,
historical currency rates, and user favorite currencies.
"""

from django.db import models
from django.contrib.auth import get_user_model


class Currency(models.Model):
    code = models.PositiveSmallIntegerField()
    text_code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "currency"


class HistoryCurrencies(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=5)
    date = models.DateTimeField()
    actualy_end = models.DateTimeField()

    class Meta:
        db_table = "history_currencies"


class FavoriteCurrency(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    class Meta:
        db_table = "favorite_currency"
