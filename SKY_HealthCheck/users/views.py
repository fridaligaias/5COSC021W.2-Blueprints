# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegistrationForm

def home(request):
    return render(request, 'users/home.html')

def register(request):
    return render(request, 'users/register.html')

def profile(request):
    return render(request, 'users/profile.html')

def login(request):
    return render(request, 'users/login.html')

def logout(request):
    return render(request, 'users/logout.html')