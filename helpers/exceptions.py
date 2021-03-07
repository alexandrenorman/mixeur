from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework import status


class WrongParameters(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Query string parameters are missing or not valid")
    default_code = "wrong_parameters"
