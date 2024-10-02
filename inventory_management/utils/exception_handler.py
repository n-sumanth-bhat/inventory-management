from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    # Call the default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        return response

    if isinstance(exc, Exception):
        # Handle unhandled exceptions
        error_message = str(exc)
        data = {
            "error": error_message
        }
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Return the standard response if no custom handling is needed
    return response
