"""
Module for a Django management
command to create a test user.

This module contains a management command class `Command`
which inherits from Django's `BaseCommand`.
The command is designed to create a test user
with predefined email and password.
"""

from django.core.management.base import BaseCommand
from user.models import User
import typing

EMAIL_TEST_USER: str = "test@mail.com"
PASSWORD_TEST_USER: str = "test_294"


class Command(BaseCommand):
    help = "Creating test user"

    def handle(self, *args: typing.Tuple, **options: typing.Dict):
        """
        Handle method for executing the command.
        This method creates a test user with the provided email and password,
        saves it to the database, and outputs a success message.
        """
        user = User(email=EMAIL_TEST_USER)
        user.set_password(raw_password=PASSWORD_TEST_USER)

        user.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully created user {user.email}"))
