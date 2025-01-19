from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.platforms.services.platform_service import PlatformService
from apps.user.models import ExchangeAccount


class TradingVolumeDataView(APIView):
    def get(self, request):
        account_id = request.query_params.get("account_id")
        if not account_id:
            return Response({"error": "account_id is required"}, status=400)

        try:
            exchange_account = ExchangeAccount.objects.get(id=account_id)
        except ExchangeAccount.DoesNotExist:
            return Response({"error": "Exchange account not found"}, status=404)

        # Get last month's data
        now = datetime.now()
        start_time = (now.replace(day=1) - timedelta(days=1)).replace(day=1)
        end_time = now.replace(day=1) - timedelta(days=1)

        try:
            volume_data = PlatformService.get_trading_volume(
                exchange_account, start_time, end_time
            )

            cashback_amount = PlatformService.get_cashback_amount(
                exchange_account, start_time, end_time
            )

            return Response(
                {
                    "trading_volume": [
                        {
                            "trading_type": data.trading_type,
                            "volume": data.trading_volume,
                            "start_time": data.start_time,
                            "end_time": data.end_time,
                        }
                        for data in volume_data
                    ],
                    "cashback_amount": cashback_amount,
                }
            )

        except ValueError as e:
            return Response({"error": str(e)}, status=400)
