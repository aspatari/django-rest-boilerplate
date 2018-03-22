from django.core.mail import send_mail

from apps.users import serializers
from . import utils


class PostRegistrationConfirmAction(utils.GenericAction):
    name = 'Post Registration Confirm email Action'
    description = 'Action for sending confirmation email after user register and confirm after access'

    def apply(self):
        user = self.get_object()
        user.is_confirmed = True
        user.save(update_fields=['is_confirmed'])

    def post_create(self):
        # TODO Add tempalted mail and use celery
        send_mail(
            subject="Confirmation Email",
            message=f'{self.obj.id}',
            from_email='support@bookmarks.com',
            recipient_list=[f'{self.obj.user.email}']
        )


class ResetPasswordAction(utils.GenericAction):
    name = 'User reset password'
    description = 'Action for resenting user password'
    serializer_class = serializers.ResetUserPasswordSerializer

    def apply(self):
        # Extract data
        user = self.get_object()
        request = self.settings.get('request')

        # Validate input data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.get('password')

        # Set data
        user.set_password(password)
        user.save(update_fields=['password'])

    def post_create(self):
        # TODO Add tempalted mail and use celery
        send_mail(
            subject="Confirmation Email",
            message=f'{self.obj.id}',
            from_email='support@bookmarks.com',
            recipient_list=[f'{self.obj.user.email}']
        )

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserialized input, and for serializing output.
        """
        serializer_class = self.serializer_class
        return serializer_class(*args, **kwargs)
