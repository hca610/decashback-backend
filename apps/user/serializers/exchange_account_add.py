from rest_framework import serializers

from apps.user.models import ExchangeAccount


class ExchangeAccountAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeAccount
        fields = ["platform_id", "account_identifier"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["user_id"] = self.context["user_id"]
        attrs["referral_id"] = self._get_referral_id()
        return attrs

    def _get_referral_id(self):
        """Find the referral id from the referral code, which get from account_identifier and platform_id"""

    def save(self):
        exchange_account = ExchangeAccount.objects.create(**self.validated_data)
        return exchange_account
