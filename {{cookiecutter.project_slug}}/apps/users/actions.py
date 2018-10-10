from rest_framework.exceptions import MethodNotAllowed
from django.conf import settings
from templated_email import send_templated_mail
from apps.users import serializers
from . import utils


class PostRegistrationConfirmAction(utils.GenericAction):
    name = "Post Registration Confirm email Action"
    description = "Action for sending confirmation email after user register and confirm after access"

    def apply(self):
        user = self.get_object()
        user.is_confirmed = True
        user.save(update_fields=["is_confirmed"])
        self.obj.delete()

    def post_create(self):
        host = getattr(settings, "CLIENT_HOST")
        url = f"{host}/user/confirm/{self.obj.id}"
        send_templated_mail(
            template_name="email-confirm-user",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.obj.user.email],
            context={"url": url},
        )


class ResetPasswordAction(utils.GenericAction):
    name = "User reset password"
    description = "Action for resenting user password"
    serializer_class = serializers.ResetUserPasswordSerializer

    def apply(self):
        # Extract data
        user = self.get_object()
        request = self.settings.get("request")

        # Validate input data
        if not request:
            raise MethodNotAllowed(method="GET")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.get("password")

        # Set data
        user.set_password(password)
        user.save(update_fields=["password"])
        self.obj.delete()

    def post_create(self):
        host = getattr(settings, "CLIENT_HOST")
        url = f"{host}/login/reset/{self.obj.id}"

        send_templated_mail(
            template_name="email-reset-password",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.obj.user.email],
            context={"url": url},
        )

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserialized input, and for serializing output.
        """
        serializer_class = self.serializer_class
        return serializer_class(*args, **kwargs)
