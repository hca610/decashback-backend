from abc import ABC, abstractmethod

from apps.user.models import ExchangeAccount


class PlatformInterface(ABC):
    """Abstract base class for trading platform interfaces"""

    @abstractmethod
    def request_base(self, method=None, url_path=None, params=None, data=None):
        """Request base method for all platform interfaces"""

    @abstractmethod
    def get_trading_volume(
        self,
        exchange_account: ExchangeAccount,
        start_time: int,
        end_time: int,
    ) -> float:
        """Get trading volume data for a platform account within a time period"""

    @abstractmethod
    def get_cashback_amount(
        self,
        exchange_account: ExchangeAccount,
        start_time: int,
        end_time: int,
    ) -> float:
        """Get cashback amount earned for a platform account within a time period"""

    @abstractmethod
    def verify_account(self, account_identifier: str) -> bool:
        """Verify if an account identifier is valid"""

    @abstractmethod
    def get_account_info(
        self, account_identifier: str, start_time: int, end_time: int
    ) -> dict:
        pass


class PlatformFactory:
    _interfaces = {}

    @classmethod
    def get_platform_cls(cls, platform_name: str) -> PlatformInterface:
        """Get platform interface for a given platform"""

        if platform_name not in cls._interfaces:
            platform_cls = cls._create_platform_cls(platform_name)
            if platform_cls:
                cls._interfaces[platform_name] = platform_cls

        return cls._interfaces.get(platform_name)

    @staticmethod
    def _create_platform_cls(platform_name: str) -> PlatformInterface:
        from apps.platforms.binance import Binance
        from apps.platforms.mexc import Mexc
        from apps.platforms.okx import Okx

        """Create new platform instance based on platform name"""

        platform_map = {
            "binance": Binance,
            "okx": Okx,
            "mexc": Mexc,
        }

        platform_cls = platform_map.get(platform_name.lower())
        if platform_cls:
            return platform_cls()
        return None
