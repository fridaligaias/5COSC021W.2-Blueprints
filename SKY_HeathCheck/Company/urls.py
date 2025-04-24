from django.urls import path

from . import views

urlpatterns = [
    path("sign-up/", views.HandleSignupForm, name = 'sign-in'),
    path("session/", views.HandleChoosingSessions, name = 'choosing-sessions'),
    
    path("Engineer/<int:id>", views.HandleChoosingSessions, name = 'engineer-profile'),
    path("TeamLeader/<int:id>", views.HandleChoosingSessions, name = 'teamleader-profile'),
]