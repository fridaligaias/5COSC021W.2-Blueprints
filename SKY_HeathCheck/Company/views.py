from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse

from Company.forms import CreateUserForm
from Company.models import Department, SessionCard

# Displays all of the necessary fields for a register/sign-up page
# region signup/register pages

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
            
      if (user != None): 
        login(request, user)
        
        if (group.name == "Engineer"):
          return redirect('engineer-profile', id = user.pk)
        if (group.name == "Team Leader"):
          return redirect('teamleader-profile')
        else:
          return redirect('teamleader-profile')
        
      
  else:
    form = CreateUserForm()
    
  return render(request, 'Company/SignupPage.html', {'form': form})

# endregion 




def ValidUsersToVote(user):
  voteGroups = ['Engineer']
  return user.is_authenticated  and user.groups.filter(name__in = voteGroups).exists()

@user_passes_test(ValidUsersToVote, login_url = "/company/sign-up/")
@login_required
def HandleChoosingSessions(request, id):
  departments = Department.objects.all()
  
  content = {'departments' : departments}
  return render(request, 'Company/Engineer.html', content)