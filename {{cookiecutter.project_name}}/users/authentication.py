from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.translation import ugettext as _


class CustomJWTAuthentication(JSONWebTokenAuthentication):
    def authenticate_credentials(self, payload):
        user = super(CustomJWTAuthentication, self).authenticate_credentials(payload)

        # Check is user  account have confirmed email
        if not user.is_confirmed:
            msg = _('User account is not confirmed.')
            raise exceptions.AuthenticationFailed(msg)

        return user
