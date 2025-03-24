from django.urls import path
from . import views

urlpatterns = [
    path('results_dashboard/', views.results_dashboard, name='results_dashboard'),
]
