from datetime import datetime
from typing import List

from apps.cashback.models import TradingVolumeData
from apps.platforms.interfaces import PlatformInterface
from apps.user.models import ExchangeAccount


class Mexc(PlatformInterface):
    def __init__(self):
        pass

    def get_trading_volume(
        self,
        exchange_account: ExchangeAccount,
        start_time: datetime,
        end_time: datetime,
    ) -> List[TradingVolumeData]:
        return []

    def get_cashback_amount(
        self,
        exchange_account: ExchangeAccount,
        start_time: datetime,
        end_time: datetime,
    ) -> float:
        return 0.0

    def verify_account(self, account_identifier: str) -> bool:
        return True
