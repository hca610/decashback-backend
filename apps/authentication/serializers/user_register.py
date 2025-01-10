import re

from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.user.models.user import User


class UserRegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate_username(self, username):
        if not re.match(r"^[a-zA-Z0-9_]{6,20}$", username):
            raise serializers.ValidationError(
                "Username must be 6-20 characters long, contain only letters, numbers, and underscores"
            )

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(_("Username is already taken"))

        return username

    def save(self):
        user = User.objects.create(
            name=self.validated_data["name"],
            username=self.validated_data["username"],
            password=make_password(self.validated_data["password"]),
        )
        return user
