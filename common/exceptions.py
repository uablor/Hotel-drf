from rest_framework.exceptions import APIException


class NotFoundError(APIException):
    status_code = 404
    default_detail = 'Resource not found.'
    default_code = 'Not_found'
