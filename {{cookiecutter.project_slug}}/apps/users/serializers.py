from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.utils.translation import ugettext as _
from rest_framework import serializers, exceptions

from . import models

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "first_name", "last_name", "username",)
 