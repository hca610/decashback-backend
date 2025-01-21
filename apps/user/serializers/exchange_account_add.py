from rest_framework import serializers

from apps.cashback.models.platform import Platform
from apps.user.models import ExchangeAccount


class ExchangeAccountAddSerializer(serializers.Serializer):
    platform_id = serializers.CharField(required=True)
    account_identifier = serializers.CharField(required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["user_id"] = self.context["user_id"]

        # validate account identifier
        platform_name = Platform.objects.get(id=attrs["platform_id"]).name
        account_identifier = attrs["account_identifier"]
        if ExchangeAccount.objects.filter(
            platform__name=platform_name,
            account_identifier=account_identifier,
        ).exists():
            raise serializers.ValidationError("Account already exists")

        return attrs

    def save(self):
        exchange_account = ExchangeAccount.objects.create(**self.validated_data)
        return exchange_account
