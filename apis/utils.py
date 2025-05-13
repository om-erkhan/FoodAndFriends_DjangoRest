# your_app/utils.py

from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if isinstance(exc, NotAuthenticated):
        return Response(
            {
                "status": {"code": 401, "success": False},
                "data": None,
                "error": "You must be authenticated to access this resource.",
                "message": "Authentication required.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return response
