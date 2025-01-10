from django.db import models

from apps.cashback.models.platform import Platform
from apps.user.models.user import User
from base.models import BaseModel


class Cashback(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    volumn = models.FloatField()
    cashback_rate = models.FloatField()
    cashback_amount = models.FloatField()

    class Meta:
        db_table = "cashbacks"
