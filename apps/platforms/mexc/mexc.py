import hashlib
import hmac
import os
from datetime import datetime

import requests
from django.core.exceptions import ValidationError
from rest_framework import status

from apps.platforms.interfaces import PlatformInterface
from apps.user.models import ExchangeAccount
from base.exception import PlatformAPIError


class Mexc(PlatformInterface):
    api_key = os.getenv("MEXC_API_KEY")
    api_secret = os.getenv("MEXC_API_SECRET")
    base_url = "https://api.mexc.com/api/v3/"

    def _generate_signature(self, params, data):
        query_string = "&".join([f"{key}={params[key]}" for key in (params.keys())])

        # Add data to query string if present
        if data:
            data_string = "&".join(
                [f"{key}={data[key]}" for key in sorted(data.keys())]
            )
            query_string = query_string + data_string

        # Generate HMAC SHA256 signature
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        return signature

    def request_base(self, method=None, url_path=None, params=None, data=None):
        params["recvWindow"] = 60000
        params["timestamp"] = int(datetime.now().timestamp() * 1000)
        params["signature"] = self._generate_signature(params, data)
        headers = {
            "X-MEXC-APIKEY": self.api_key,
            "Content-Type": "application/json",
        }

        try:
            full_url = f"{self.base_url}{url_path}"
            response = requests.request(
                method, full_url, headers=headers, params=params, data=data
            )
        except Exception as e:
            raise PlatformAPIError(f"Failed to {method.upper()} {url_path}: {e}")

        return response

    def get_trading_volume(
        self,
        exchange_account: ExchangeAccount,
        start_time: int,
        end_time: int,
    ) -> float:
        account_info = self.get_account_info(
            exchange_account.account_identifier, start_time, end_time
        )
        return account_info.get("tradingAmount")

    def get_cashback_amount(
        self,
        exchange_account: ExchangeAccount,
        start_time: int,
        end_time: int,
    ) -> float:
        return 0.0

    def verify_account(self, account_identifier: str) -> bool:
        url_path = "rebate/affiliate/referral"
        params = {"uid": account_identifier}
        try:
            response = self.request_base(method="GET", url_path=url_path, params=params)
            if (
                response.status_code == status.HTTP_200_OK
                and response.json().get("data", {}).get("totalCount") > 0
            ):
                if any(
                    item.get("uid") == account_identifier
                    for item in response.json().get("data", {}).get("resultList", [])
                ):
                    return True
        except Exception as e:
            raise PlatformAPIError(f"Failed to verify account: {e}")

        return False

    def get_account_info(
        self, account_identifier: str, start_time: int, end_time: int
    ) -> dict:
        url_path = "rebate/affiliate/referral"
        params = {
            "uid": account_identifier,
            "startTime": start_time,
            "endTime": end_time,
        }
        try:
            response = self.request_base(method="GET", url_path=url_path, params=params)
            if response.status_code != status.HTTP_200_OK:
                raise ValidationError(f"Failed to get account info: {response.json()}")

            if response.json().get("data", {}).get("totalCount") > 0:
                if any(
                    item.get("uid") == account_identifier
                    for item in response.json().get("data", {}).get("resultList", [])
                ):
                    account_info = (
                        response.json().get("data", {}).get("resultList", [])[0]
                    )
                    return account_info

        except Exception as e:
            raise PlatformAPIError(f"Failed to get account info: {e}")
