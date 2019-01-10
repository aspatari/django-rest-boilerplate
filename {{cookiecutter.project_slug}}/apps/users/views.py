from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, permissions, generics, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.common.views import CustomViewSetMixin, CustomSerializerViewSetMixin
from . import serializers, models


class UserViewSet(CustomViewSetMixin, viewsets.ModelViewSet):
    queryset = get_user_model().objects
    serializer_class = serializers.UserDetailSerializer