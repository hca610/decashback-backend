from datetime import datetime, timedelta

from rest_framework import serializers

from apps.platforms.services.platform_service import PlatformService
from apps.user.models import ExchangeAccount


class ExchangeAccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeAccount
        fields = [
            "id",
            "account_identifier",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        current_month_start_time = int(datetime.now().replace(day=1).timestamp() * 1000)
        current_month_end_time = int(datetime.now().replace(day=31).timestamp() * 1000)
        last_month_start_time = int(
            (datetime.now() - timedelta(days=30)).replace(day=1).timestamp() * 1000
        )
        last_month_end_time = int(
            (datetime.now() - timedelta(days=30)).replace(day=31).timestamp() * 1000
        )

        data["platform"] = instance.platform.name
        data["current_month_trading_volume"] = PlatformService.get_trading_volume(
            instance, current_month_start_time, current_month_end_time
        )
        data["last_month_trading_volume"] = PlatformService.get_trading_volume(
            instance, last_month_start_time, last_month_end_time
        )
        return data
