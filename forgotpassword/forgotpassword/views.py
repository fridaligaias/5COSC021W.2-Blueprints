from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import models
from .forms import ForgotPasswordForm
from .models import Account
from django.http import HttpResponse

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email_or_username = form.cleaned_data['email_or_username']
            role = request.POST.get('role')

            try:
                account = Account.objects.filter(
                    (models.Q(emailAddress=email_or_username) | models.Q(userName=email_or_username)),
                    accountRole=role
                ).first()
                
                if account:
                    request.session['reset_email'] = account.emailAddress
                    request.session['reset_role'] = role
                    return redirect('reset_password')
                else:
                    messages.error(request, "Invalid username or email.")
                    return render(request, 'forgot_password.html', {'form': form})
            
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return render(request, 'forgot_password.html', {'form': form})
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'forgot_password.html', {'form': form})

def reset_password(request):
   reset_email = request.session.get('reset_email')
   reset_role = request.session.get('reset_role')
   
   if not reset_email or not reset_role:
       messages.error(request, "Invalid reset request.")
       return redirect('forgot_password')
   
   if request.method == 'POST':
       new_password = request.POST.get('new_password')
       confirm_password = request.POST.get('confirm_password')
       
       if not new_password or not confirm_password:
           messages.error(request, "Please enter both password fields.")
           return render(request, 'reset_password.html')
       
       if new_password != confirm_password:
           messages.error(request, "Passwords do not match.")
           return render(request, 'reset_password.html')
       
       try:
           account = Account.objects.get(
               emailAddress=reset_email, 
               accountRole=reset_role
           )
           
           account.set_password(new_password)
           account.save()
           
           messages.success(request, "Password reset successfully.")
           
           
           request.session['password_reset_success'] = True
           
           
           from django.urls import reverse
           return render(request, 'reset_password.html', {
               'redirect_delay': True,
               'redirect_url': reverse('login_page'),
               'delay_seconds': 10,
               'email': reset_email,  
               'role': reset_role     
           })
       
       except Account.DoesNotExist:
           messages.error(request, f"No account found with email {reset_email} and role {reset_role}")
           return redirect('forgot_password')
   
   
   if request.session.get('password_reset_success'):
       if 'reset_email' in request.session:
           del request.session['reset_email']
       if 'reset_role' in request.session:
           del request.session['reset_role']
       del request.session['password_reset_success']
       
       
       from django.urls import reverse
       return redirect(reverse('login_page'))
   
   
   return render(request, 'reset_password.html', {
       'email': reset_email,
       'role': reset_role
   })
   
def login_page(request):
   return HttpResponse("Login page")

def home(request):
    return HttpResponse("Home Page")