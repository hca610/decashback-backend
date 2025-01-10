from django.db import models

from apps.cashback.models.platform import Platform
from apps.user.models.user import User
from base.models import BaseModel


class ExchangeAccount(BaseModel):
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    account_identifier = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    referral = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="referred_ids"
    )

    class Meta:
        db_table = "exchange_accounts"

    def get_cashback_amount(self):
        pass
