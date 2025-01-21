import copy

from jwt.exceptions import ExpiredSignatureError
from rest_framework import status
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as base_exception_handler
from sentry_sdk import capture_exception


def handle_error(error: str | dict | list, field_default: str = None):
    response_data_custom = {
        "success": False,
        "field": field_default,
        "error_code": None,
        "message": None,
        "detail": None,
        "additional_infos": {},
    }

    if isinstance(error, str):
        response_data_custom["message"] = str(error)

        if isinstance(error, ErrorDetail):
            response_data_custom["error_code"] = error.code

    elif isinstance(error, dict):
        for field, message in error.items():
            return handle_error(message, field_default=field)

    elif isinstance(error, list):
        if len(error) > 0:
            return handle_error(error[0], field_default=field_default)

    return response_data_custom


def exception_handler(exc, context):
    if isinstance(exc, ExpiredSignatureError):
        response_data_custom = {
            "success": False,
            "message": "Signature has expired.",
        }
        return Response(
            data=response_data_custom,
            status=status.HTTP_401_UNAUTHORIZED,
        )

    response = base_exception_handler(exc, context)
    if response is not None:
        try:
            if isinstance(exc, ValidationError):
                errors = copy.deepcopy(response.data)

                response_data_custom = handle_error(errors)
                response_data_custom["detail"] = errors
                if hasattr(exc, "get_infos"):
                    response_data_custom["additional_infos"] = exc.get_infos()

                response_custom = Response(
                    data=response_data_custom, status=response.status_code
                )

                return response_custom
        except Exception as e:
            capture_exception(e)

    return response


class PlatformAPIError(Exception):
    pass
