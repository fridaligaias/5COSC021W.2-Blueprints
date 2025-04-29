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
from .models import Team, Session, SessionCard, Vote, Department, Account
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.db.models import Avg, F, FloatField
from django.db.models.functions import Coalesce



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
  
    print("Request method:", request.method)
    print("Cookies:", request.COOKIES)
    print("POST data:", request.POST)
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            login(request, user)
            
            # Check user group and redirect accordingly
            user_group = request.user.groups.first().name if request.user.groups.exists() else None
            
            if user_group == "Department Leader":
                try:
                    # Get the user's department ID
                    # account = Account.objects.get(accountID=user)
                    # department_id = account.departmentID.departmentID
                    
                    # Redirect directly to department leader dashboard with the user's department
                    return redirect('log-in-department', userid=user.pk)
                
                except Account.DoesNotExist:
                    messages.error(request, "Account not found. Please contact an administrator.")
                    return redirect('log-in')
            
            # Other role redirects remain the same
            elif user_group == "Engineer":
              return redirect('log-in-department', userid=user.pk)

            elif user_group == "Team Leader":
                try:
                    # Get the user's account and team
                    account = Account.objects.get(accountID=user)
                    
                    # Check if user has selected a team
                    if hasattr(account, 'teamID') and account.teamID:
                        return redirect('team_leader_dashboard', teamid=account.teamID.teamID)
                    else:
                        # If no team is selected, redirect to team selection
                        return redirect('log-in-department', userid=user.pk)
                except Account.DoesNotExist:
                    messages.error(request, "Account not found. Please contact an administrator.")
                    return redirect('log-in')
              
            elif user_group == "Senior Engineer":
                return redirect("senior_manager_dashboard")
            
            # Default redirect if no specific group handling
            return redirect('log-in-department', userid=user.pk)
    
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

# Permission check functions
def ValidUsersToVote(user):
    voteGroups = ['Engineer', 'Team Leader']
    return user.is_authenticated and user.groups.filter(name__in = voteGroups).exists()

def ValidUsersToDepartmentLogin(user):
    voteGroups = ['Engineer', 'Team Leader', 'Department Leader']
    return user.is_authenticated and user.groups.filter(name__in = voteGroups).exists()

def ValidUsersToTeamLogin(user):
    voteGroups = ['Engineer', 'Team Leader']
    return user.is_authenticated and user.groups.filter(name__in = voteGroups).exists()

def ValidEngineer(user):
    voteGroups = ['Engineer']
    return user.is_authenticated and user.groups.filter(name__in = voteGroups).exists()

def ValidTeamLeader(user):
    voteGroups = ['Team Leader']
    return user.is_authenticated and user.groups.filter(name__in = voteGroups).exists()

def ValidDepartmentLeader(user):
    voteGroups = ['Department Leader']
    return user.is_authenticated and user.groups.filter(name__in = voteGroups).exists()

def ValidSeniorManager(user):
    voteGroups = ['Senior Engineer']
    return user.is_authenticated and user.groups.filter(name__in = voteGroups).exists()

def is_department_leader(user):
    """
    Check if the user is a Department Leader
    """
    return user.is_authenticated and user.groups.filter(name='Department Leader').exists()

@user_passes_test(ValidUsersToDepartmentLogin, login_url = "/company/sign-up/")
@login_required
def HandleLoginDepartmentForm(request, userid):
  departmentForm = SelectDepartment()
  
  if (request.method == 'POST'):
    departmentForm = SelectDepartment(request.POST)
    if (departmentForm.is_valid()):
      department = departmentForm.cleaned_data['department']
      request.user.account.departmentID = department
      request.user.account.save()
      
      if (request.user.groups.first().name == "Engineer"):
        return redirect('log-in-team', userid = request.user.pk)
      elif (request.user.groups.first().name == "Team Leader"):
        return redirect('log-in-team', userid = request.user.pk)
      elif (request.user.groups.first().name == "Department Leader"):
        # Redirect department leader to dashboard
        return redirect('department_leader_dashboard_with_id', dept_id= request.user.account.departmentID.departmentID)
    
  return render(request, 'Company/SignupDepartmentPage.html', {'departmentForm': departmentForm} )

@user_passes_test(ValidUsersToTeamLogin, login_url = "/company/sign-up/")
@login_required
def HandleLoginTeamForm(request, userid):
  teamForm = SelectTeam(departmentID = request.user.account.departmentID.departmentID)
  
  if (request.method == 'POST'):
    teamForm = SelectTeam(request.POST, departmentID = request.user.account.departmentID.departmentID)
    if (teamForm.is_valid()):
      team = teamForm.cleaned_data['team']
      
      if (request.user.groups.first().name == "Engineer"):
        return redirect('engineer-profile', userid = request.user.pk, teamid = team.teamID)
      elif (request.user.groups.first().name == "Team Leader"):
        return redirect('team-leader-profile', userid = request.user.pk, teamid = team.teamID)
    
  return render(request, 'Company/SignupTeamPage.html', {'teamForm': teamForm} )

@user_passes_test(ValidEngineer, login_url = "/company/sign-up/")
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
  
@user_passes_test(ValidTeamLeader, login_url = "/company/sign-up/")
@login_required
def HandleTeamLeaderProfile(request, userid, teamid):
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
        'teamid': teamid,  

    }
    return render(request, 'Company/TeamLeader.html', context)
  
@user_passes_test(ValidDepartmentLeader, login_url = "/company/sign-up/")
@login_required
def HandleDepartmentLeaderProfile(request, userid):
    """
    Legacy function - can be removed or updated to redirect to the new dashboard
    """
    return redirect('department_leader_redirect')
  
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

@login_required
@user_passes_test(is_department_leader)
def department_leader_dashboard(request):
    """
    Show the dashboard for the Department Leader based on their department
    """
    try:
        # Get the user's account and associated department
        account = Account.objects.get(accountID=request.user)
        user_department = account.departmentID
        
        # Only show the department that this leader is responsible for
        departments = Department.objects.filter(departmentID=user_department.departmentID)
    except Account.DoesNotExist:
        departments = Department.objects.none()
    
    departments_data = []
    for department in departments:
        # Get all teams in this department
        teams = Team.objects.filter(departmentID=department)
        
        # Get total members in this department
        department_members = Account.objects.filter(departmentID=department)
        department_members_count = department_members.count()
        
        # Create member list for display in modal
        member_list = []
        for member in department_members:
            user = member.accountID
            member_list.append({
                'full_name': f"{user.first_name} {user.last_name}",
                'username': user.username,
                'email': user.email
            })
        
        # Calculate department-wide metrics
        total_sessions = Session.objects.filter(teamID__in=teams).count()
        total_cards = SessionCard.objects.filter(sessionID__teamID__in=teams).count()
        total_possible_votes = total_cards * department_members_count
        total_actual_votes = Vote.objects.filter(sessionCardID__sessionID__teamID__in=teams).count()
        
        if total_possible_votes > 0:
            department_completion = (total_actual_votes / total_possible_votes) * 100
        else:
            department_completion = 0
            
        # Get data for each team in the department
        teams_data = []
        for team in teams:
            # Count team members (assuming all department members can access all teams)
            team_members = Account.objects.filter(departmentID=department)
            team_members_count = team_members.count()
            
            # Get active sessions for this team
            sessions = Session.objects.filter(teamID=team).order_by('-sessionStartData')
            
            # Calculate team metrics
            team_cards = SessionCard.objects.filter(sessionID__teamID=team).count()
            team_possible_votes = team_cards * team_members_count
            team_actual_votes = Vote.objects.filter(sessionCardID__sessionID__teamID=team).count()
            
            if team_possible_votes > 0:
                team_completion = (team_actual_votes / team_possible_votes) * 100
            else:
                team_completion = 0
                
            # Get recent sessions (top 3)
            recent_sessions = []
            for session in sessions[:3]:  # Limit to 3 most recent sessions
                session_cards = SessionCard.objects.filter(sessionID=session).count()
                session_votes = Vote.objects.filter(sessionCardID__sessionID=session).count()
                session_possible_votes = session_cards * team_members_count
                
                if session_possible_votes > 0:
                    session_completion = (session_votes / session_possible_votes) * 100
                else:
                    session_completion = 0
                    
                recent_sessions.append({
                    'session': session,
                    'completion': session_completion,
                    'cards_count': session_cards,
                    'votes_count': session_votes,
                    'possible_votes': session_possible_votes
                })
            
            teams_data.append({
                'team': team,
                'members_count': team_members_count,
                'sessions_count': sessions.count(),
                'cards_count': team_cards,
                'votes_count': team_actual_votes,
                'possible_votes': team_possible_votes,
                'completion': team_completion,
                'recent_sessions': recent_sessions
            })
            
        # Add all department data to the list
        departments_data.append({
            'department': department,
            'members_count': department_members_count,
            'teams_count': teams.count(),
            'sessions_count': total_sessions,
            'cards_count': total_cards,
            'votes_count': total_actual_votes,
            'possible_votes': total_possible_votes,
            'completion': department_completion,
            'teams': teams_data,
            'member_list': member_list
        })
    
    context = {
        'departments_data': departments_data,
        'user_full_name': f"{request.user.first_name} {request.user.last_name}",
    }
    
    return render(request, 'department_leader_dashboard.html', context)

# For specific department view (without login requirement, for testing purposes)
@login_required(login_url='log-in')
def department_leader_dashboard_with_id(request, dept_id):
    """
    Show the dashboard for a specific department (for testing or direct access)
    """
    # Get the specific department by ID
    department = get_object_or_404(Department, departmentID=dept_id)
    departments = Department.objects.filter(departmentID=dept_id)
    
    # Rest of function is the same as above...
    departments_data = []
    for department in departments:
        # Get all teams in this department
        teams = Team.objects.filter(departmentID=department)
        
        # Get total members in this department
        department_members = Account.objects.filter(departmentID=department)
        department_members_count = department_members.count()
        
        # Create member list for display in modal
        member_list = []
        for member in department_members:
            user = member.accountID
            member_list.append({
                'full_name': f"{user.first_name} {user.last_name}",
                'username': user.username,
                'email': user.email
            })
        
        # Calculate department-wide metrics
        total_sessions = Session.objects.filter(teamID__in=teams).count()
        total_cards = SessionCard.objects.filter(sessionID__teamID__in=teams).count()
        total_possible_votes = total_cards * department_members_count
        total_actual_votes = Vote.objects.filter(sessionCardID__sessionID__teamID__in=teams).count()
        
        if total_possible_votes > 0:
            department_completion = (total_actual_votes / total_possible_votes) * 100
        else:
            department_completion = 0
            
        # Get data for each team in the department
        teams_data = []
        for team in teams:
            # Count team members (assuming all department members can access all teams)
            team_members = Account.objects.filter(departmentID=department)
            team_members_count = team_members.count()
            
            # Get active sessions for this team
            sessions = Session.objects.filter(teamID=team).order_by('-sessionStartData')
            
            # Calculate team metrics
            team_cards = SessionCard.objects.filter(sessionID__teamID=team).count()
            team_possible_votes = team_cards * team_members_count
            team_actual_votes = Vote.objects.filter(sessionCardID__sessionID__teamID=team).count()
            
            if team_possible_votes > 0:
                team_completion = (team_actual_votes / team_possible_votes) * 100
            else:
                team_completion = 0
                
            # Get recent sessions (top 3)
            recent_sessions = []
            for session in sessions[:3]:  # Limit to 3 most recent sessions
                session_cards = SessionCard.objects.filter(sessionID=session).count()
                session_votes = Vote.objects.filter(sessionCardID__sessionID=session).count()
                session_possible_votes = session_cards * team_members_count
                
                if session_possible_votes > 0:
                    session_completion = (session_votes / session_possible_votes) * 100
                else:
                    session_completion = 0
                    
                recent_sessions.append({
                    'session': session,
                    'completion': session_completion,
                    'cards_count': session_cards,
                    'votes_count': session_votes,
                    'possible_votes': session_possible_votes
                })
            
            teams_data.append({
                'team': team,
                'members_count': team_members_count,
                'sessions_count': sessions.count(),
                'cards_count': team_cards,
                'votes_count': team_actual_votes,
                'possible_votes': team_possible_votes,
                'completion': team_completion,
                'recent_sessions': recent_sessions
            })
            
        # Add all department data to the list
        departments_data.append({
            'department': department,
            'members_count': department_members_count,
            'teams_count': teams.count(),
            'sessions_count': total_sessions,
            'cards_count': total_cards,
            'votes_count': total_actual_votes,
            'possible_votes': total_possible_votes,
            'completion': department_completion,
            'teams': teams_data,
            'member_list': member_list
        })
    
    context = {
        'departments_data': departments_data,
        'user_full_name': request.user.first_name + " " + request.user.last_name if request.user.is_authenticated else "Guest User",
    }
    
    return render(request, 'Company/department_leader_dashboard.html', context)

@never_cache
def user_logout(request):
    logout(request)
    response = redirect('log-in')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
  
@login_required(login_url='log-in')
def senior_manager_dashboard(request):
    try:
        # Get all departments (Senior Manager can see everything)
        departments = Department.objects.all()
        
        departments_data = []
        
        for department in departments:
            # Get all teams in this department
            department_teams = Team.objects.filter(departmentID=department)
            
            teams_data = []
            for team in department_teams:
                # Get team members
                team_members = Account.objects.filter(departmentID=department)
                team_members_count = team_members.count()
                
                # Prepare sessions data
                sessions_data = []
                sessions = Session.objects.filter(teamID=team).order_by('-sessionStartData')
                
                for session in sessions:
                    # Get session cards
                    cards = SessionCard.objects.filter(sessionID=session)
                    
                    cards_data = []
                    total_potential_votes = team_members_count * len(cards)
                    total_actual_votes = 0
                    
                    for card in cards:
                        # Get vote details for each card
                        votes = Vote.objects.filter(sessionCardID=card)
                        
                        card_data = {
                            'card_id': card.sessionCardID,
                            'green_description': card.greenDescription,
                            'amber_description': card.amberDescription,
                            'red_description': card.redDescription,
                            'green_votes': card.greenVote,
                            'amber_votes': card.amberVote,
                            'red_votes': card.redVote,
                            'voters_count': votes.count(),
                            'voters_percentage': (votes.count() / team_members_count) * 100 if team_members_count > 0 else 0,
                            'pending_votes': team_members_count - votes.count()
                        }
                        
                        cards_data.append(card_data)
                        total_actual_votes += votes.count()
                    
                    # Calculate session completion
                    session_completion = (total_actual_votes / total_potential_votes) * 100 if total_potential_votes > 0 else 0
                    
                    sessions_data.append({
                        'session': session,
                        'cards_data': cards_data,
                        'actual_votes': total_actual_votes,
                        'potential_total_votes': total_potential_votes,
                        'completion_percentage': session_completion
                    })
                
                # Append team data to this department's teams list
                teams_data.append({
                    'team': team,
                    'members_count': team_members_count,
                    'sessions': sessions_data
                })
            
            # Add department and its teams to departments_data
            departments_data.append({
                'departmentID': department.departmentID,
                'departmentName': department.departmentName,
                'teams': teams_data
            })
        
        context = {
            'departments_data': departments_data,
            'user_full_name': f"{request.user.first_name} {request.user.last_name}"
        }
        
        return render(request, 'Company/senior_engineer_dashboard.html', context)
    
    except Exception as e:
        # Log the error or handle it appropriately
        print(f"Error in senior manager dashboard: {e}")
        return redirect('log-in')

@never_cache
def senior_manager_logout(request):
    logout(request)
    response = redirect('log-in')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required(login_url='log-in')
@user_passes_test(ValidTeamLeader)
def team_leader_dashboard(request, teamid):
    try:
        # Get the team that this leader is responsible for
        team = get_object_or_404(Team, teamID=teamid)
        
        # Get team members
        department = team.departmentID
        team_members = Account.objects.filter(departmentID=department)
        team_members_count = team_members.count()
        
        # Create member list for display in modal
        member_list = []
        for member in team_members:
            user = member.accountID
            member_list.append({
                'full_name': f"{user.first_name} {user.last_name}",
                'username': user.username,
                'email': user.email
            })
        
        # Get sessions for this team
        sessions = Session.objects.filter(teamID=team).order_by('-sessionStartData')
        
        # Calculate team metrics
        team_cards = SessionCard.objects.filter(sessionID__teamID=team).count()
        team_possible_votes = team_cards * team_members_count
        team_actual_votes = Vote.objects.filter(sessionCardID__sessionID__teamID=team).count()
        
        if team_possible_votes > 0:
            team_completion = (team_actual_votes / team_possible_votes) * 100
        else:
            team_completion = 0
        
        # Get data for each session
        sessions_data = []
        for session in sessions:
            # Get session cards
            cards = SessionCard.objects.filter(sessionID=session)
            
            cards_data = []
            total_potential_votes = team_members_count * len(cards)
            total_actual_votes = 0
            
            for card in cards:
                # Get vote details for each card
                votes = Vote.objects.filter(sessionCardID=card)
                
                card_data = {
                    'card_id': card.sessionCardID,
                    'green_description': card.greenDescription,
                    'amber_description': card.amberDescription,
                    'red_description': card.redDescription,
                    'green_votes': card.greenVote,
                    'amber_votes': card.amberVote,
                    'red_votes': card.redVote,
                    'voters_count': votes.count(),
                    'voters_percentage': (votes.count() / team_members_count) * 100 if team_members_count > 0 else 0,
                    'pending_votes': team_members_count - votes.count()
                }
                
                # Get voters details
                voters_list = []
                for vote in votes:
                    user = vote.userID
                    voters_list.append({
                        'full_name': f"{user.first_name} {user.last_name}",
                        'vote_type': 'Green' if vote.greenVote else ('Amber' if vote.amberVote else 'Red'),
                        'comment': vote.comment
                    })
                
                card_data['voters'] = voters_list
                cards_data.append(card_data)
                total_actual_votes += votes.count()
            
            # Calculate session completion
            session_completion = (total_actual_votes / total_potential_votes) * 100 if total_potential_votes > 0 else 0
            
            sessions_data.append({
                'session': session,
                'cards_data': cards_data,
                'actual_votes': total_actual_votes,
                'potential_total_votes': total_potential_votes,
                'completion_percentage': session_completion
            })
        
        context = {
            'team': team,
            'department': department,
            'members_count': team_members_count,
            'member_list': member_list,
            'sessions_count': sessions.count(),
            'cards_count': team_cards,
            'votes_count': team_actual_votes,
            'possible_votes': team_possible_votes,
            'completion': team_completion,
            'sessions': sessions_data,
            'user_full_name': f"{request.user.first_name} {request.user.last_name}"
        }
        
        return render(request, 'Company/team_leader_dashboard.html', context)
    
    except Exception as e:
        # Log the error or handle it appropriately
        print(f"Error in team leader dashboard: {e}")
        return redirect('log-in')
    

@login_required
def summary_view(request):
    
    # 1. Grab the first name for the header
    firstname = request.user.first_name

    # 2. Fetch all Vote records for this user
    user_votes = Vote.objects.filter(user=request.user).select_related('sessionCardID')

    # 3. Render 'summary.html' with exactly the context your template uses
    return render(request, 'summary.html', {
        'firstname': firstname,
        'user_votes': user_votes,
    })
