from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    detail = None
    status_code = None

    def __init__(self, detail, code):
        super().__init__(detail, code)
        self.detail = detail
        self.status_code = code


class NotFoundException(BaseCustomException):
    def __init__(self, error="Record Not Found", desc=None):
        detail = UtilClass.create_exception_detail(error, desc)
        super().__init__(detail, status.HTTP_404_NOT_FOUND)


class AlreadyExistsException(BaseCustomException):
    def __init__(self, error="Record Already Exists", desc=None):
        detail = UtilClass.create_exception_detail(error, desc)
        super().__init__(detail, status.HTTP_409_CONFLICT)

class ValidationException(BaseCustomException):
    def __init__(self, error="Validation Error", desc=None):
        detail = UtilClass.create_exception_detail(error, desc)
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)


class AuthenticationFailed(BaseCustomException):
    def __init__(self, error="Authentication Failed", desc=None):
        detail = UtilClass.create_exception_detail(error, desc)
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR)

class UtilClass():
    def create_exception_detail(error, desc):
        detail = {
            "error": error,
            "description": desc
        }
        return detail