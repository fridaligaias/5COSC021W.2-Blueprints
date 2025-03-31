from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


def SigninPage(request):
  form = UserCreationForm(request.POST)
  return render(request, "Company/Signin.html", {'form': form})
