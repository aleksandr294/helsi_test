"""
Module defines the URL patterns for
currency-related APIs in the Django application.
It maps each API view to a specific URL pattern,
specifying the endpoint and corresponding view class.
"""

from django.urls import path
from currencies import views

urlpatterns = [
    path(
        "",
        views.CurrenciesListAPIView.as_view(),
        name="currencies",
    ),
    path(
        "current",
        views.CurrentCurrenciesListAPIView.as_view(),
        name="current",
    ),
    path("history", views.HistoryCurrenciesListAPIView.as_view(), name="history"),
    path(
        "favorite/create",
        views.CreateFavoriteCurrencyAPIView.as_view(),
        name="create_favorite",
    ),
    path(
        "favorite/delete/<int:currency_id>",
        views.DeleteFavoriteCurrencyAPIView.as_view(),
        name="delete_favorite",
    ),
    path(
        "favorite/current",
        views.CurrentFavoriteCurrenciesListAPIView.as_view(),
        name="favorite_current",
    ),
]
