from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from .forms import ForgotPasswordForm

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email_or_username = form.cleaned_data['email_or_username']
            
            try:
                # Look up user directly in User model using either email or username
                user = User.objects.filter(
                    Q(email=email_or_username) | Q(username=email_or_username)
                ).first()
                
                if user:
                    # Generate password reset token
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    
                    # Store in session (for simple approach) or use the token in email
                    request.session['reset_uid'] = uid
                    request.session['reset_token'] = token
                    
                    # For a more secure approach, you'd send an email with a link containing the token
                    # rather than storing in session
                    
                    # Redirect to reset page
                    return redirect('reset_password')
                else:
                    messages.error(request, "No account found with this email or username.")
                    return render(request, 'forgot_password.html', {'form': form})
            
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return render(request, 'forgot_password.html', {'form': form})
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'forgot_password.html', {'form': form})

def reset_password(request):
    uid = request.session.get('reset_uid')
    token = request.session.get('reset_token')
    
    if not uid or not token:
        messages.error(request, "Invalid reset request.")
        return redirect('forgot_password')
    
    try:
        # Decode the user ID and get the user
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
        
        # Verify the token
        if not default_token_generator.check_token(user, token):
            messages.error(request, "Invalid reset link or it has expired.")
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
            
            # Set the new password
            user.set_password(new_password)
            user.save()
            
            messages.success(request, "Password reset successfully.")
            
            # Clean up session
            if 'reset_uid' in request.session:
                del request.session['reset_uid']
            if 'reset_token' in request.session:
                del request.session['reset_token']
            
            request.session['password_reset_success'] = True
            
            return render(request, 'reset_password.html', {
                'redirect_delay': True,
                'redirect_url': reverse('login_page'),
                'delay_seconds': 10,
                'email': user.email
            })
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('forgot_password')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('forgot_password')
    
    return render(request, 'reset_password.html', {
        'email': user.email if 'user' in locals() else ''
    })

def login_page(request):
    return HttpResponse("Login page")

def home(request):
    return HttpResponse("Home Page")