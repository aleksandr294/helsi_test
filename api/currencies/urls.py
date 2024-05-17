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
]
