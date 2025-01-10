from django.urls import include, path

urlpatterns = [
    path("api/v1/auth/", include("apps.authentication.urls")),
    path("api/v1/user/", include("apps.user.urls")),
    path("api/v1/cashback/", include("apps.cashback.urls")),
    path("api/v1/transaction/", include("apps.transaction.urls")),
]
