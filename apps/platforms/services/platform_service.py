from datetime import datetime

from apps.cashback.models.platform import Platform
from apps.platforms.interfaces.platform_factory import PlatformFactory
from apps.user.models import ExchangeAccount


class PlatformService:
    @staticmethod
    def _get_platform(platform):
        """Get platform or raise ValueError if not found"""
        platform = PlatformFactory.get_platform(platform)
        if not platform:
            platform_name = platform.name if hasattr(platform, "name") else platform
            raise ValueError(f"No platform found for platform {platform_name}")
        return platform

    @staticmethod
    def get_trading_volume(
        exchange_account: ExchangeAccount, start_time: datetime, end_time: datetime
    ):
        """Get trading volume data for a platform account"""
        platform = PlatformService._get_platform(exchange_account.platform)
        return platform.get_trading_volume(exchange_account, start_time, end_time)

    @staticmethod
    def get_cashback_amount(
        exchange_account: ExchangeAccount, start_time: datetime, end_time: datetime
    ) -> float:
        """Get cashback amount for a platform account"""
        platform = PlatformService._get_platform(exchange_account.platform)
        return platform.get_cashback_amount(exchange_account, start_time, end_time)

    @staticmethod
    def verify_account(platform_name: str, account_identifier: str) -> bool:
        """Verify if an account identifier is valid for a given platform"""
        platform = Platform.objects.filter(name=platform_name).first()
        if not platform:
            raise ValueError(f"Platform {platform_name} not found")

        platform = PlatformService._get_platform(platform)
        return platform.verify_account(account_identifier)
