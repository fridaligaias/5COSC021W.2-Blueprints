from django.urls import path

from . import views

urlpatterns = [
    path("sign-in", views.SigninPage, name = 'sign-in')
]
