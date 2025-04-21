from django import forms
from django.contrib.auth.models import User
from .models import Account

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
        
        try:
            account = Account.objects.filter(emailAddress=email_or_username).first()
            
            if not account:
                account = Account.objects.filter(userName=email_or_username).first()
            
            if not account:
                raise forms.ValidationError("No account found with this email or username.")
            
            return email_or_username
        
        except Account.DoesNotExist:
            raise forms.ValidationError("No account found with this email or username.")