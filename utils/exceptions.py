from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError


def ValidationErrorHandler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError) and not response:
        response = Response({'errors': exc.message_dict}, status=status.HTTP_400_BAD_REQUEST)

    return response