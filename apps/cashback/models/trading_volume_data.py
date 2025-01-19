from django.db import models

from apps.user.models import ExchangeAccount
from base.models import BaseModel


class TradingType(models.TextChoices):
    SPOT = "spot", "Spot"
    FUTURES = "futures", "Futures"
    MARGIN = "margin", "Margin"


class TradingVolumeData(BaseModel):
    exchange_account = models.ForeignKey(ExchangeAccount, on_delete=models.CASCADE)
    trading_volume = models.FloatField()
    trading_type = models.CharField(max_length=10, choices=TradingType.choices)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        db_table = "trading_volume_data"
