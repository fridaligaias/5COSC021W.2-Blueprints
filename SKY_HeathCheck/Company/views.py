from django.shortcuts import render

from Company.forms import CreateUserForm

# Create your views here.
def HandleSignupForm(request):
  form = CreateUserForm()
  
  return render(request, 'Company/SignupPage.html', {'form': form})