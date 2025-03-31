from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

#Management and Engineer login functions

def managementLogin(request):
    return HttpResponse('<h1>Log In</h1>')

def engineerLogin(request):
    return HttpResponse('<h1>Log In</h1>')
