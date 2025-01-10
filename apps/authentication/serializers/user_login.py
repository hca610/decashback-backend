from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.authentication.utils import generate_access_token
from apps.user.models.user import User


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def login(self):
        username = self.validated_data["username"]
        password = self.validated_data["password"]

        try:
            user = User.objects.filter(username=username).get()
        except User.DoesNotExist:
            raise serializers.ValidationError(_("Username is not found"))

        if not user.check_password(password):
            raise serializers.ValidationError(_("Password is incorrect"))

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        return {
            "user": user.to_dict(),
            "access_token": generate_access_token(user),
        }
