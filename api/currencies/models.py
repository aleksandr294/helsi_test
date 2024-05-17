from django.db import models
import datetime


class Currency(models.Model):
    code = models.PositiveSmallIntegerField()
    text_code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "currency"


class HistoryCurrencies(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=5)
    date = models.DateTimeField(default=datetime.datetime.utcnow())
    actualy_end = models.DateTimeField()

    class Meta:
        db_table = "history_currencies"
