from django.urls import path

from . import views

urlpatterns = [
    path(
        "trading-volume", views.TradingVolumeDataView.as_view(), name="trading-volume"
    ),
]
