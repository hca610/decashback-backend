from rest_framework import serializers

from apps.affiliate.models import Affiliate
from apps.cashback.models import Platform
from apps.user.models import User


class AffiliateCreateSerializer(serializers.Serializer):
    platform_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    ref_code = serializers.CharField()

    def validate(self, attrs):
        platform_id = attrs.get("platform_id")
        user_id = attrs.get("user_id")

        try:
            Platform.objects.get(id=platform_id)
            User.objects.get(id=user_id)
        except Platform.DoesNotExist:
            raise serializers.ValidationError("Platform does not exist")
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        return attrs

    def create(self, validated_data):
        platform_id = validated_data.get("platform_id")
        user_id = validated_data.get("user_id")
        ref_code = validated_data.get("ref_code")

        affiliate = Affiliate.objects.create(
            platform_id=platform_id,
            user_id=user_id,
            ref_code=ref_code,
        )

        return affiliate
