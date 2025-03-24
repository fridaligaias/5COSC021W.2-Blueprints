from django.urls import path
from . import views

urlpatterns = [
    path('choose_session/', views.choose_session, name='choose_session'),
    path('vote/<int:session_id>/', views.vote, name='vote'),
    path('vote_summary/', views.vote_summary, name='vote_summary'),
]
