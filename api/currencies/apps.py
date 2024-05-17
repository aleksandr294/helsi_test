"""
Module defining the configuration
for the 'currencies' Django app.

This module provides the configuration
for the 'currencies' app in a Django project.
It specifies the default auto field
to use for models and sets the name of the app.

"""

from django.apps import AppConfig


class CurrenciesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "currencies"
