from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class ProfileNotFound(APIException):
    status_code = 404
    default_detail = _("The requested profile does not exist.")


class NotYourProfile(APIException):
    status_code = 403
    default_detail = _("You can't edit a profile that doesn't belong to you")
