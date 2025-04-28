from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("sign-up/", views.HandleSignupForm, name = 'sign-in'),
    path("login-in/", views.HandleLogin, name = 'log-in'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path("sign-up/<int:userid>/department", views.HandleLoginDepartmentForm, name = 'log-in-department'),
    path("sign-up/<int:userid>/team", views.HandleLoginTeamForm, name = 'log-in-team'),
    
    path("engineer/<int:userid>/<int:teamid>", views.HandleEngineerProfile, name = 'engineer-profile'),
    path("teamleader/<int:userid>/<int:teamid>", views.HandleTeamLeaderProfile, name = 'team-leader-profile'),
    path("departmentleader/<int:userid>", views.HandleDepartmentLeaderProfile, name = 'department-leader-profile'),
    path("seniormanager/", views.HandleEngineerProfile, name = 'senior-manager-profile'),
    
    path("voting/<int:userid>/<int:teamid>/<int:sessionid>", views.HandleVoting, name = 'voting-form'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)