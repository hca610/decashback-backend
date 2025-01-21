from rest_framework import serializers

from apps.user.models import ExchangeAccount


class ExchangeAccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeAccount
        fields = "__all__"
