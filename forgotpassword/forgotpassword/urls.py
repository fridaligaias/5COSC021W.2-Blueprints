from django.urls import path
from . import views

urlpatterns = [
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('login/', views.login_page, name='login_page'),
    path('', views.home, name = "Home page")
]