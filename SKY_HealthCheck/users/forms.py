from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role']
