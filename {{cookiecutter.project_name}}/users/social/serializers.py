from allauth.socialaccount.helpers import complete_social_login
from django.urls import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from requests.exceptions import HTTPError
from rest_framework import serializers


class SocialLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(required=False, allow_blank=True)

    def get_social_login(self, adapter, app, token, response):
        """
        :param adapter: allauth.socialaccount Adapter subclass.
            Usually OAuthAdapter or Auth2Adapter
        :param app: `allauth.socialaccount.SocialApp` instance
        :param token: `allauth.socialaccount.SocialToken` instance
        :param response: Provider's response for OAuth1. Not used in the
        :returns: A populated instance of the
            `allauth.socialaccount.SocialLoginView` instance
        """
        request = self.context.get('request')
        social_login = adapter.complete_login(request, app, token, response=response)
        social_login.token = token
        return social_login

    def validate(self, attrs):
        view = self.context.get('view')
        request = self.context.get('request')

        if not view:
            raise serializers.ValidationError(
                _("View is not defined, pass it as a context variable")
            )

        adapter_class = getattr(view, 'adapter_class', None)
        if not adapter_class:
            raise serializers.ValidationError(_("Define adapter_class in view"))

        adapter = adapter_class(request)
        app = adapter.get_provider().get_app(request)

        # Case 1: We received the access_token
        if attrs.get('access_token'):
            token = access_token = attrs.get('access_token')

        # Case 2: We received the authorization code
        elif attrs.get('code'):
            self.callback_url = getattr(view, 'callback_url', None)
            self.client_class = getattr(view, 'client_class', None)

            if not self.callback_url:
                raise serializers.ValidationError(
                    _("Define callback_url in view")
                )
            if not self.client_class:
                raise serializers.ValidationError(
                    _("Define client_class in view")
                )

            code = attrs.get('code')

            provider = adapter.get_provider()
            scope = provider.get_scope(request)
            client = self.client_class(
                request,
                app.client_id,
                app.secret,
                adapter.access_token_method,
                adapter.access_token_url,
                self.callback_url,
                scope
            )
            token = client.get_access_token(code)
            access_token = token['access_token']

        else:
            raise serializers.ValidationError(
                _("Incorrect input. access_token or code is required."))

        social_token = adapter.parse_token({'access_token': access_token})
        social_token.app = app

        try:
            login = self.get_social_login(adapter, app, social_token, token)
            complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError(_("Incorrect value"))
        except NoReverseMatch:
            # ToDo refactor
            # Works for now, until better solution
            raise serializers.ValidationError(_("User with same email already exists"))

        user = login.account.user
        if user and not user.is_confirmed:
            user.is_confirmed = True
            user.save()
        attrs['user'] = user

        return attrs
