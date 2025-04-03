from django.shortcuts import render
from django.contrib.auth import authenticate, login

from Company.forms import CreateUserForm

# Create your views here.
def HandleSignupForm(request):
  form = CreateUserForm()
  if (request == 'POST'):
    form = CreateUserForm(request.POST)
    
    if (form.is_valid()):
      form.save()
      username = form.cleaned_data['username']
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password1']
      
      
      user = authenticate(username = username, 
                          password = password, 
                          email = email,
                          first_name = first_name,
                          last_name = last_name)
      
      print(user)
      
      login(request, user)
      
  else:
    form = CreateUserForm()
      
  
  return render(request, 'Company/SignupPage.html', {'form': form})