from django.conf.urls import include
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainSlidingView, TokenRefreshSlidingView, TokenVerifyView
from . import views

router = SimpleRouter(trailing_slash=False)
router.register("users", viewset=views.UserViewSet)

urlpatterns = [
                  path("users/login", TokenObtainSlidingView.as_view(), name="token_obtain"),
                  path("users/token/refresh", TokenRefreshSlidingView.as_view(), name="token_refresh"),

              ] + router.urls
