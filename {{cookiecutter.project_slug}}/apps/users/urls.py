from django.conf.urls import include
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from . import views

router = SimpleRouter(trailing_slash=False)

router.register('users', views.GeneralUserViewSet)

urlpatterns = [
    path('users/login', views.ObtainJSONWebToken.as_view(), name='jwt-login'),
    path('users/register', views.UserRegistrationView.as_view(), name='user-registration'),
    path('users/profile', views.UserProfileView.as_view(), name='user-profile'),
    path('users/password/reset', views.UserResetPasswordView.as_view(), name='user-password-reset'),
    path('users/password/modify', views.UserModifyPasswordView.as_view(), name='user-password-modify'),
    path('users/transaction/<uuid:pk>/apply', views.UserTransactionApplyView.as_view(), name='user-transaction-apply'),
    path('users/token/verify', verify_jwt_token),
    path('users/token/refresh', refresh_jwt_token),
    path("", include(router.urls)),
]
