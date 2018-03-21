from urllib.parse import urlencode

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.vk.views import VKOAuth2Adapter
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import serializers


class SocialLoginView(GenericAPIView):
    """
    Class used for social authentications
    """
    serializer_class = serializers.SocialLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response({"token": user._generate_jwt_token()}, status=status.HTTP_200_OK)

    def get(self, request):
        return redirect(self.token_url + urlencode(self.params))


class FacebookLoginView(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'http://localhost:8008/v1/social/facebook'
    token_url = 'https://www.facebook.com/v2.11/dialog/oauth?'
    params = {
        'client_id'    : settings.FACEBOOK_CLIENT_ID,
        'redirect_uri' : 'http://localhost:4200/facebook',
        'scope'        : 'email,public_profile',
        'response_type': 'token',
    }


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'http://localhost:8008/v1/social/google'
    token_url = 'https://accounts.google.com/o/oauth2/v2/auth?'
    params = {
        'client_id'    : settings.GOOGLE_CLIENT_ID,
        'redirect_uri' : 'http://localhost:4200/google',
        'scope'        : 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'token',
    }


class VKLoginView(SocialLoginView):
    adapter_class = VKOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'http://localhost:8008/v1/social/vk'
    token_url = 'https://oauth.vk.com/authorize?'
    params = {
        'client_id'    : settings.VK_CLIENT_ID,
        'redirect_uri' : 'http://localhost:4200/vk',
        'response_type': 'token',
    }
