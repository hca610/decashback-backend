from django.db import models

from base.models import BaseModel


class PlatformCashbackInterval(models.TextChoices):
    DAILY = "daily", "Daily"
    WEEKLY = "weekly", "Weekly"
    MONTHLY = "monthly", "Monthly"


class Platform(BaseModel):
    name = models.CharField(max_length=255)
    cashback_interval = models.CharField(
        max_length=10, choices=PlatformCashbackInterval.choices
    )

    class Meta:
        db_table = "platforms"
