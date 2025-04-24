from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class CreateUserForm(UserCreationForm):
  
  group = forms.ModelChoiceField(Group.objects.all(), required = True)
  
  class Meta:
    model = User 
    fields = ['username', 'first_name', 'last_name', 'email']