from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login

from Company.forms import CreateUserForm
from Company.models import SessionCard

# Create your views here.
def HandleSignupForm(request):
  form = CreateUserForm()
  
  if (request.method == 'POST'):
    form = CreateUserForm(request.POST)
    
    if (form.is_valid()):
      form.save()
      username = form.cleaned_data['username']
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password1']
      group = form.cleaned_data['group']
      
      
      user = authenticate(username = username, 
                          password = password)
      
      user.first_name = first_name
      user.last_name = last_name
      user.email = email
      user.groups.add(group)
            
      if (user != None): login(request, user)
      
  else:
    form = CreateUserForm()
      
  
  return render(request, 'Company/SignupPage.html', {'form': form})

def HandleDepartment(request, departmentName):
  return HttpResponse(f"This is from the request from the department " + departmentName)