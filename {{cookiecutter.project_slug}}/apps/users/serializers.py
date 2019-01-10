from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.utils.translation import ugettext as _
from rest_framework import serializers, exceptions

from apps.users.utils import send_user_password_to_mail
from . import models


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "first_name", "last_name", "username", "role")
        extra_kwargs = {
            "first_name": {"allow_blank": False, "required": True},
            "last_name": {"allow_blank": False, "required": True},
        }

    def create(self, validated_data):
        user_model = self.Meta.model

        password = user_model.objects.make_random_password()
        validated_data["password"] = password

        user = user_model.objects.create_user(**validated_data)

        send_user_password_to_mail(user.username, password)

        return user


class UserEditingSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "first_name", "last_name", "role")


class UserModifyPasswordSerializer(serializers.Serializer):
    """ This serializer is used for modifying user password """

    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        pass


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ChangePasswordRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChangePasswordRequests
        fields = ("id", "is_approved")


class UserDetailSerializer(serializers.ModelSerializer):
    change_password_requests = ChangePasswordRequestSerializer(read_only=True, many=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "first_name", "last_name", "username", "role", "lang", "change_password_requests")


class UserProfileEditiongSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "first_name", "last_name", "lang",)
