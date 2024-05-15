"""
The `urls` module configures the URL
routing for the Django application.
This module contains the `urlpatterns` list, which defines the mapping between
URLs and view functions or class-based views.
It includes paths for serving the API schema using `drf_spectacular`'s views:
`SpectacularAPIView`, `SpectacularSwaggerView`, and `SpectacularRedocView`.
Additionally, it includes a path for the user API endpoints,
which are configured in a separate
`user.urls` module using the `include` function.
"""

from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/user/", include("user.urls")),
]
