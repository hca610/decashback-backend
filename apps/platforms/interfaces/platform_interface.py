from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from apps.cashback.models import TradingVolumeData
from apps.user.models import ExchangeAccount


class PlatformInterface(ABC):
    """Abstract base class for trading platform interfaces"""

    @abstractmethod
    def request_base(self, method, url_path, params, data):
        """Request base method for all platform interfaces"""

    @abstractmethod
    def get_trading_volume(
        self,
        exchange_account: ExchangeAccount,
        start_time: datetime,
        end_time: datetime,
    ) -> List[TradingVolumeData]:
        """Get trading volume data for a platform account within a time period"""

    @abstractmethod
    def get_cashback_amount(
        self,
        exchange_account: ExchangeAccount,
        start_time: datetime,
        end_time: datetime,
    ) -> float:
        """Get cashback amount earned for a platform account within a time period"""

    @abstractmethod
    def verify_account(self, account_identifier: str) -> bool:
        """Verify if an account identifier is valid"""
