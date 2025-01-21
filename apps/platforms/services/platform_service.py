from datetime import datetime

from apps.platforms.interfaces import PlatformFactory
from apps.user.models import ExchangeAccount


class PlatformService:
    @staticmethod
    def _get_platform_cls(platform_name):
        """Get platform or raise ValueError if not found"""
        platform_cls = PlatformFactory.get_platform_cls(platform_name)
        if not platform_cls:
            raise ValueError(f"No platform class found for platform {platform_name}")
        return platform_cls

    @staticmethod
    def get_trading_volume(
        exchange_account: ExchangeAccount, start_time: int, end_time: int
    ):
        """Get trading volume data for a platform account"""
        platform_cls = PlatformService._get_platform_cls(exchange_account.platform.name)
        return platform_cls.get_trading_volume(exchange_account, start_time, end_time)

    @staticmethod
    def get_cashback_amount(
        exchange_account: ExchangeAccount, start_time: datetime, end_time: datetime
    ) -> float:
        """Get cashback amount for a platform account"""
        platform = PlatformService._get_platform_cls(exchange_account.platform)
        return platform.get_cashback_amount(exchange_account, start_time, end_time)

    @staticmethod
    def verify_account(platform_name: str, account_identifier: str) -> bool:
        """Verify if an account identifier is valid for a given platform"""
        platform_cls = PlatformService._get_platform_cls(platform_name)
        return platform_cls.verify_account(account_identifier)

    @staticmethod
    def get_account_info(
        platform_name: str, account_identifier: str, start_time: int, end_time: int
    ) -> dict:
        """Get account info for a given platform"""
        platform_cls = PlatformService._get_platform_cls(platform_name)
        return platform_cls.get_account_info(account_identifier, start_time, end_time)
