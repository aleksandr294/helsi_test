"""
Module for configuring URLs related to
authentication using JWT in Django.
This module contains URL patterns for handling
token-based authentication using JWT (JSON Web Tokens).
It includes endpoints for obtaining a token pair
(access token and refresh token), refreshing a token,
and verifying the validity of a token.
"""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
