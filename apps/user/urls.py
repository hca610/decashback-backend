from django.urls import path

from . import views

urlpatterns = [
    path(
        "exchange-account/add",
        views.ExchangeAccountAddView.as_view(),
        name="exchange-account-add",
    ),
    path(
        "exchange-account/list",
        views.ExchangeAccountListView.as_view(),
        name="exchange-account-list",
    ),
    path(
        "exchange-account/detail/<int:pk>",
        views.ExchangeAccountDetailView.as_view(),
        name="exchange-account-detail",
    ),
]
