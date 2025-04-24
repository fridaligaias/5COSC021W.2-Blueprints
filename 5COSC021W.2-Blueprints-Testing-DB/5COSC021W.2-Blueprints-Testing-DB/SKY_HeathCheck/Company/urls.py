from django.urls import path

from . import views

urlpatterns = [
    path("sign-in/", views.HandleSignupForm, name = 'sign-in')
]