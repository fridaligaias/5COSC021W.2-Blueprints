from django.urls import path

from . import views

urlpatterns = [
    path("sign-up/", views.HandleSignupForm, name = 'sign-in'),
    path("sign-up/<int:userid>/department", views.HandleSignupDepartmentForm, name = 'sign-in-department'),
    path("sign-up/<int:userid>/team", views.HandleSignupTeamForm, name = 'sign-in-team'),
    path("engineer/<int:userid>/<int:teamid>", views.HandleEngineerProfile, name = 'engineer-profile'),
    path("voting/<int:userid>/<int:teamid>/<int:sessionid>", views.HandleVoting, name = 'voting-form'),
]