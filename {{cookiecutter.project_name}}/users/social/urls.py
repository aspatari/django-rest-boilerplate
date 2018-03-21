from django.urls import path

from . import views

urlpatterns = [
    path('facebook', views.FacebookLoginView.as_view()),
    path('google', views.GoogleLoginView.as_view()),
    path('vk', views.VKLoginView.as_view()),
]
