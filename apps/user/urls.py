from django.urls import path

from . import views

urlpatterns = [
    path(
        "exchange-account/add",
        views.ExchangeAccountAddView.as_view(),
        name="exchange-account-add",
    ),
]
