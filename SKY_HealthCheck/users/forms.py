from django import forms
from .models import User  # or the relevant model

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # adjust to your fields
