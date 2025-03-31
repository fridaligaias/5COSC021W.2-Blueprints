from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

#Management and Engineer login functions

def managementLogin(request):
    return render (request , 'management_login.html')

def engineerLogin(request):
    return render (request , 'engineer_login.html')
