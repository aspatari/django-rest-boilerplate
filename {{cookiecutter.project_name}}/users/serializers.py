from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers, exceptions
from rest_framework.generics import get_object_or_404
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import password_validation
from . import models


class CustomJSONWebTokenSerializer(JSONWebTokenSerializer):
    """ Serializer is modified for handling is_confirmed on user model """

    def validate(self, attrs):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = {"detail": _('User account is disabled.')}
                    raise serializers.ValidationError(msg)
                if not user.is_confirmed:
                    msg = {"detail": _('User account is not confirmed.')}
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


class GeneralUserSerializer(serializers.ModelSerializer):
    """ Serializer is used for listing general info about user"""

    class Meta:
        model = get_user_model()
        fields = ("id", "username",)


class UserRegisterSerializer(serializers.ModelSerializer):
    """ Serializer is user for user registration """
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password")

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        user_model = self.Meta.model

        user = user_model.objects.create_user(**validated_data)

        user.create_transaction("PostRegistrationConfirmAction")

        return user


class ResetPasswordInitSerializer(serializers.Serializer):
    """ Serializer is user for user reset password process """
    email = serializers.EmailField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        email = validated_data.get('email')
        user = get_object_or_404(get_user_model(), email=email)
        user.create_transaction('ResetPasswordAction')
        return email


class ResetUserPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value


class UserModifyPasswordSerializer(serializers.Serializer):
    """ This serializer is used for modifying user password """
    old_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        old_password, new_password = validated_data.values()

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save(update_fields=['password'])
        else:
            msg = {'detail': _('Wrong Input data')}
            raise exceptions.ValidationError(msg)
        return user

    def update(self, instance, validated_data):
        pass


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializer is used for  Retrieving and Updating user profile  """

    class Meta:
        model = models.Profile
        exclude = ('id', 'user', 'created_at', 'updated_at')
