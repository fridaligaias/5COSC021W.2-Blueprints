from django.urls import path

from . import views

urlpatterns = [
    path("sign-up/", views.HandleSignupForm, name = 'sign-in'),
    path("<str:departmentName>/", views.HandleDepartment, name = 'voting')
]