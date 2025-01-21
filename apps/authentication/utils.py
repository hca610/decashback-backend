import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings

from apps.user.models import User


def jwt_payload_handler(user):
    payload = {
        "user_id": user.pk,
        "name": user.name,
        "is_active": user.is_active,
    }

    return payload


def generate_access_token(user):
    payload = jwt_payload_handler(user)
    access_token = jwt.encode(payload, settings.SECRET_KEY)
    return access_token


def generate_refresh_token(user):
    payload = jwt_payload_handler(user)
    refresh_token = jwt.encode(payload, settings.SECRET_KEY)
    return refresh_token


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.META.get("HTTP_AUTHORIZATION", b"")
        if not auth or auth == b"":
            raise AuthenticationFailed(
                {
                    "success": False,
                    "message": "Invalid token header. No credentials provided.",
                    "status": status.HTTP_401_UNAUTHORIZED,
                }
            )
        user, auth_token = self.authenticate_credentials(auth)

        return user, auth_token

    def authenticate_credentials(self, token):
        key = api_settings.SIGNING_KEY
        try:
            decoded_token = jwt.decode(token, key, algorithms=["HS256"])
        except Exception:
            raise AuthenticationFailed(
                {
                    "success": False,
                    "message": "Invalid token header. No credentials provided.",
                    "status": status.HTTP_401_UNAUTHORIZED,
                }
            )
        if not decoded_token.get("is_active"):
            raise AuthenticationFailed(
                {
                    "success": False,
                    "message": "User inactive or deleted.",
                    "status": status.HTTP_403_FORBIDDEN,
                }
            )

        return User.from_jwt_decoded_token(decoded_token), decoded_token

    def has_permission(self, request, view):
        return request.user
