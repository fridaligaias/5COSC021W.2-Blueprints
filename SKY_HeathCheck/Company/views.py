from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db.models import Q
from django.contrib import messages
from Company.forms import CreateUserForm, ForgotPasswordForm, SelectDepartment, SelectSession, SelectTeam, VotingForm
from Company.models import SessionCard, Vote

# Displays all of the necessary fields for a register/sign-up page
# region signup/register pages

def HandleSignupForm(request):
  signupForm = CreateUserForm()
  
  if (request.method == 'POST'):
    signupForm = CreateUserForm(request.POST)
    
    if (signupForm.is_valid()):
      signupForm.save()
      username = signupForm.cleaned_data['username']
      first_name = signupForm.cleaned_data['first_name']
      last_name = signupForm.cleaned_data['last_name']
      email = signupForm.cleaned_data['email']
      password = signupForm.cleaned_data['password1']
      group = signupForm.cleaned_data['group']
      
      user = authenticate(username = username, 
                          password = password)
      
      user.first_name = first_name
      user.last_name = last_name
      user.email = email
      user.groups.add(group)
      user.save()
      user.account.save()
      
      if (user != None): 
        return redirect('log-in')
        
  else:
    signupForm = CreateUserForm()
    
  return render(request, 'Company/SignupPage.html', {'signupForm': signupForm} )

# endregion 

def HandleLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            
            login(request, user)
            if (request.user.groups.first().name == "Engineer"):
              return redirect('log-in-department', userid = user.pk)
            if (request.user.groups.first().name == "Team Leader"):
              return redirect('log-in-department', userid = user.pk)
            if (request.user.groups.first().name == "DepartmentLeader"):
              return redirect('log-in-department', userid = user.pk)
    else:
        form = AuthenticationForm()
    return render(request, 'Company/LoginPage.html', {'form': form})

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
                    return render(request, 'Company/forgot_password.html', {'form': form})
            
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return render(request, 'Company/forgot_password.html', {'form': form})
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'Company/forgot_password.html', {'form': form})

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
                return render(request, 'Company/reset_password.html')
            
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, 'Company/reset_password.html')
            
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
            
            return render(request, 'Company/reset_password.html', {
                'redirect_delay': True,
                'redirect_url': reverse('log-in'),
                'delay_seconds': 10,
                'email': user.email
            })
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('forgot_password')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('forgot_password')
    
    return render(request, 'Company/reset_password.html', {
        'email': user.email if 'user' in locals() else ''
    })

def ValidUsersToVote(user):
  voteGroups = ['Engineer', 'Team Leader']
  return user.is_authenticated  and user.groups.filter(name__in = voteGroups).exists()

@user_passes_test(ValidUsersToVote, login_url = "/company/sign-up/")
@login_required
def HandleLoginDepartmentForm(request, userid):
  departmentForm = SelectDepartment()
  
  if (request.method == 'POST'):
    departmentForm = SelectDepartment(request.POST)
    if (departmentForm.is_valid()):
      department = departmentForm.cleaned_data['department']
      request.user.account.departmentID = department
      request.user.account.save()
      
      return redirect('log-in-team', userid = request.user.pk)
    
  return render(request, 'Company/SignupDepartmentPage.html', {'departmentForm': departmentForm} )

@user_passes_test(ValidUsersToVote, login_url = "/company/sign-up/")
@login_required
def HandleLoginTeamForm(request, userid):
  teamForm = SelectTeam(departmentID = request.user.account.departmentID.departmentID)
  
  if (request.method == 'POST'):
    teamForm = SelectTeam(request.POST, departmentID = request.user.account.departmentID.departmentID)
    if (teamForm.is_valid()):
      team = teamForm.cleaned_data['team']
      
      return redirect('engineer-profile', userid = request.user.pk, teamid = team.teamID)
    
  return render(request, 'Company/SignupTeamPage.html', {'teamForm': teamForm} )

@user_passes_test(ValidUsersToVote, login_url = "/company/sign-up/")
@login_required
def HandleEngineerProfile(request, userid, teamid):
    username = request.user.username
    sessionForm = SelectSession(teamID = teamid)
    
    if (request.method == 'POST'):
      sessionForm = SelectSession(request.POST, teamID = teamid)
      if (sessionForm.is_valid()):
        session = sessionForm.cleaned_data['session']
        
        return redirect('voting-form', userid = userid, teamid = teamid, sessionid = session.sessionID)
      
    context = {
			'username': username,
   		'sessionForm': sessionForm,
   
		}
    return render(request, 'Company/Engineer.html', context)
  
@user_passes_test(ValidUsersToVote, login_url = "/company/sign-up/")
@login_required
def HandleVoting(request, userid, teamid, sessionid):
  if request.method == 'POST':
    form = VotingForm(request.POST)
    if form.is_valid():
        session_card_id = form.cleaned_data['session_card_id']
        vote_type = form.cleaned_data['vote_type']
        comment = form.cleaned_data['comment']  # Get the comment
        card = get_object_or_404(SessionCard, sessionCardID = session_card_id)

				# Check if user already voted on this card
        already_voted = Vote.objects.filter(sessionCardID = card, userID = request.user).exists()
        
        if not already_voted:
                # Update SessionCard totals
          if vote_type == 'green': card.greenVote += 1
          elif vote_type == 'amber': card.amberVote += 1
          elif vote_type == 'red': card.redVote += 1
          card.save()

					# Save user's individual Vote record
          Vote.objects.create(
							sessionCardID = card,
							userID = request.user,
							greenVote = 1 if vote_type == 'green' else 0,
							amberVote = 1 if vote_type == 'amber' else 0,
							redVote = 1 if vote_type == 'red' else 0,
              comment = comment or ''
					)
          
        total_cards = SessionCard.objects.filter(sessionID = sessionid).count()
        total_votes = Vote.objects.filter(userID = request.user, sessionCardID__sessionID = sessionid).count()

        if total_votes >= total_cards:
          # User voted on all cards — redirect!
          return redirect('engineer-profile', userid = request.user.pk, teamid = teamid)
                
  cards = SessionCard.objects.filter(sessionID = sessionid)
  forms_list = [VotingForm(initial={'session_card_id': card.sessionCardID}) for card in cards]
  cards_forms = zip(cards, forms_list)
  return render(request, 'Company/VotingPage.html', {'cards': cards, 'forms_list': cards_forms})

