from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q

class ForgotPasswordForm(forms.Form):
    email_or_username = forms.CharField(
        max_length=254, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Username or Email address',
            'class': 'form-control'
        })
    )

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data['email_or_username']
        
        # Look up the user directly in the User model
        user = User.objects.filter(
            Q(username=email_or_username) | Q(email=email_or_username)
        ).first()
        
        if not user:
            raise ValidationError("No account found with this email or username.")
            
        return email_or_username