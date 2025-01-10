from django.db import models

from apps.cashback.models.platform import Platform
from base.models import BaseModel


class CashbackRate(BaseModel):
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=255)
    cashback_rate = models.FloatField()

    class Meta:
        db_table = "cashback_rates"
