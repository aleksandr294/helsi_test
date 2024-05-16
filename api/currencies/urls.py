from django.urls import path
from currencies import views

urlpatterns = [
    path(
        "current",
        views.CurrentCurrenciesListAPIView.as_view(),
        name="current",
    ),
]
