from apps.cashback.models import Platform
from apps.platforms.binance import Binance
from apps.platforms.interfaces import PlatformInterface
from apps.platforms.mexc import Mexc
from apps.platforms.okx import Okx


class PlatformFactory:
    _interfaces = {}

    @classmethod
    def get_platform(cls, platform: Platform) -> PlatformInterface:
        """Get platform interface for a given platform"""

        if platform.name not in cls._interfaces:
            interface = cls._create_platform(platform.name)
            if interface:
                cls._interfaces[platform.name] = interface

        return cls._interfaces.get(platform.name)

    @staticmethod
    def _create_platform(platform_name: str) -> PlatformInterface:
        """Create new platform instance based on platform name"""

        platform_map = {
            "binance": Binance,
            "okx": Okx,
            "mexc": Mexc,
        }

        platform_class = platform_map.get(platform_name.lower())
        if platform_class:
            return platform_class()
        return None
