from django.db import models

from apps.user.models import ExchangeAccount
from base.models import BaseModel


class TradingVolumeData(BaseModel):
    exchange_account = models.ForeignKey(ExchangeAccount, on_delete=models.CASCADE)
    trading_volume = models.FloatField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        db_table = "trading_volume_datas"
