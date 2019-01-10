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
    custom_serializer_classes = {
        "create": serializers.UserCreationSerializer,
        "update": serializers.UserEditingSerializer,
        "partial_update": serializers.UserEditingSerializer,
    }


class UserPasswordViewSet(CustomViewSetMixin, viewsets.GenericViewSet):
    queryset = models.ChangePasswordRequests.objects
    custom_serializer_classes = {
        "forgot": serializers.ForgotPasswordSerializer,
        "set": serializers.UserModifyPasswordSerializer,
    }

    custom_permission_classes = {
        "forgot": (permissions.AllowAny,),
        "reset": (permissions.IsAuthenticated,),
        "set": (permissions.AllowAny,),
    }

    @swagger_auto_schema(
        tags=["password"],
        responses={"201": "New Change Password Request Created", "202": "Already have a Change Password Request"},
    )
    @action(methods=["post"], detail=False)
    def forgot(self, request, *args, **kwargs):
        username = request.data.get("username")
        user = get_object_or_404(get_user_model().objects, username=username)

        return self.__password_change_reqeust(user)

    @swagger_auto_schema(
        tags=["password"],
        responses={"201": "New Change Password Request Created", "202": "Already have a Change Password Request"},
    )
    @action(methods=["get"], detail=False)
    def reset(self, request, *args, **kwargs):
        user = self.request.user
        return self.__password_change_reqeust(user)

    @swagger_auto_schema(tags=["password"])
    @action(methods=["post"], detail=True, name="Set Password")
    def set(self, request, pk, *args, **kwargs):
        """Set New Password"""
        change_password_request = self.get_object()
        if change_password_request.is_approved:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            password = serializer.save().get("password")

            user = change_password_request.for_user

            user.set_password(password)
            user.save(update_fields=["password"])
            change_password_request.delete()
            return Response(status=status.HTTP_200_OK)

        return Response({"message": "Request is not approved"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @swagger_auto_schema(tags=["password"])
    @action(methods=["get"], detail=True)
    def approve(self, request, *args, **kwargs):
        """Approve Change Password Request"""
        self.get_object().approve()
        return Response()

    @swagger_auto_schema(tags=["password"])
    @action(methods=["get"], detail=True)
    def decline(self, request, *args, **kwargs):
        """Approve Change Password Request"""
        self.get_object().decline()
        return Response()

    def __password_change_reqeust(self, user):
        if not user.change_password_requests.exists():
            user.change_password_requests.create()

            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_202_ACCEPTED)


class MeView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    custom_serializer_classes = {
        "get": serializers.UserDetailSerializer,
        "patch": serializers.UserProfileEditiongSerializer,
    }

    def get_serializer_class(self):
        """ Return the class to use for serializer w.r.t to the request method."""
        try:
            return self.custom_serializer_classes[self.request.method.lower()]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)

    @swagger_auto_schema(request_body=serializers.UserProfileEditiongSerializer)
    def patch(self, *args, **kwargs):
        return self.partial_update(*args, **kwargs)

    def get_object(self):
        return self.request.user
