"""
Module for a Django management
command to create a test user.

This module contains a management command class `Command`
which inherits from Django's `BaseCommand`.
The command is designed to create a test user
with predefined email and password.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import typing
from api import settings


class Command(BaseCommand):
    help = "Creating test user"

    def handle(self, *args: typing.Tuple, **options: typing.Dict):
        """
        Handle method for executing the command.
        This method creates a test user with the provided email and password,
        saves it to the database, and outputs a success message.
        """
        User = get_user_model()
        user, is_created = User.objects.get_or_create(email=settings.EMAIL_TEST_USER)

        if is_created:
            user.set_password(raw_password=settings.PASSWORD_TEST_USER)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created user {user.email}")
            )
        else:
            self.stdout.write(self.style.SUCCESS("User is created"))
