"""
Module for defining the custom user model and its manager in Django.
This module contains the `User` model, which inherits from Django's
`AbstractBaseUser`, and the `UserManager` class,
which inherits from Django's `BaseUserManager`.
These classes are used to create and manage user accounts in the application.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import typing


class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        password: typing.Optional[str] = None,
    ) -> "User":
        """
        Creates and returns a new user.

        Args:
            email (str): Email address of the user.
            password (str, optional): Password of the user. Defaults to None.

        Raises:
            ValueError: If email is not provided.

        Returns:
            User: The created user.

        """
        if not email:
            raise ValueError("User must have email ")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: typing.Optional[str] = None,
    ) -> "User":
        """
        Creates and returns a new superuser.

        Args:
            email (str): Email address of the superuser.
            password (str, optional): Password of the superuser. Defaults to None.

        Returns:
            User: The created superuser.

        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = "email"

    def __str__(self) -> models.EmailField:
        """
        Returns the email address of the user.

        Returns:
            str: Email address of the user.

        """
        return self.email

    def has_perm(self, perm: str, obj: object = None) -> bool:
        """
        Returns True if the user has the specified permission.

        This method is required by Django's authentication system.

        Args:
            perm (str): The permission string.
            obj (object, optional): The object to check permission against.
            Defaults to None.

        Returns:
            bool: True if the user has the permission, False otherwise.

        """
        return True

    def has_module_perms(self, app_label: str) -> bool:
        """
        Returns True if the user has permissions to access the given app_label.


        This method is required by Django's authentication system.

        Args:
            app_label (str): The label of the app to check permission for.


        Returns:
            bool: True if the user has permissions, False otherwise.

        """
        return True

    class Meta:
        db_table = "user"
