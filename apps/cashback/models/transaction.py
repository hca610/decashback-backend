from django.db import models

from apps.user.models.exchange_account import ExchangeAccount
from base.models import BaseModel


class TransactionStatus(models.IntegerChoices):
    PENDING = 100, "Pending"
    COMPLETED = 200, "Completed"
    FAILED = 400, "Failed"


class TransactionType(models.IntegerChoices):
    CASHBACK = 1, "Cashback"
    AFFILIATE_BONUS = 2, "Affiliate Bonus"


class Transaction(BaseModel):
    exchange_account = models.ForeignKey(ExchangeAccount, on_delete=models.CASCADE)
    type = models.IntegerField(choices=TransactionType.choices)
    status = models.IntegerField(choices=TransactionStatus.choices)
    amount = models.FloatField()
    additional_info = models.JSONField(
        default=dict
    )  # info about trading volume or referral

    class Meta:
        db_table = "transactions"
