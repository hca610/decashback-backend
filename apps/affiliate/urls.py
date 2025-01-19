from django.urls import path

from . import views

urlpatterns = [
    path("create", views.AffiliateCreateView.as_view(), name="create-affiliate"),
]
