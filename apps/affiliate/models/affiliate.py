from django.db import models

from apps.cashback.models.platform import Platform
from apps.user.models import ExchangeAccount, User
from base.models import BaseModel


class Affiliate(BaseModel):
    ref_code = models.CharField(max_length=20, unique=True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # Add field for exchange account which receive money from affiliate program
    receive_account = models.ForeignKey(
        ExchangeAccount, on_delete=models.CASCADE, null=True
    )

    class Meta:
        db_table = "affiliates"
