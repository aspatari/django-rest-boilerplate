from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework_jwt.views import JSONWebTokenAPIView

from . import models, serializers


class GeneralUserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.GeneralUserSerializer


class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = serializers.CustomJSONWebTokenSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = get_user_model().objects
    serializer_class = serializers.UserRegisterSerializer


class UserTransactionApplyView(generics.GenericAPIView):
    """ View for applying transactions for users"""
    queryset = models.Transaction.objects
    serializer_class = serializers.UserRegisterSerializer

    def get(self, request, *args, **kwargs):

        transaction = self.get_object()
        try:
            transaction.apply()
        except transaction.ExpiredTransaction:
            msg = _("This transaction was expired")
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        transaction = self.get_object()
        try:
            transaction.apply(*args, request=request, **kwargs)
        except transaction.ExpiredTransaction:
            msg = _("This transaction was expired")
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class UserResetPasswordView(generics.GenericAPIView):
    """ Init user password reset procedure"""
    serializer_class = serializers.ResetPasswordInitSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class UserModifyPasswordView(generics.GenericAPIView):
    """ Modify Password for authenticated user"""
    serializer_class = serializers.UserModifyPasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve and Update user profile  """
    serializer_class = serializers.UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile
