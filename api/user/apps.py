"""
The `user` module provides configuration for 
the user application within the Django framework.
This module contains the `UserConfig` class, 
which is a subclass of Django's `AppConfig`.
The `UserConfig` class is used to configure 
the user application within a Django project.
"""

from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"
