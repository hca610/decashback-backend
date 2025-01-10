from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from base.models import BaseModel


class User(BaseModel, AbstractUser):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)
    referral_code = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "users"

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @staticmethod
    def from_jwt_decoded_token(decoded_token):
        try:
            obj = User.get_from_cache(decoded_token["user_id"])
        except User.DoesNotExist:
            raise AuthenticationFailed(
                {
                    "success": False,
                    "message": "User inactive or deleted",
                    "status": status.HTTP_403_FORBIDDEN,
                }
            )

        return obj

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
