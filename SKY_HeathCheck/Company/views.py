from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group

from Company.forms import CreateUserForm, SelectDepartment, SelectSession, SelectTeam, VotingForm
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
        return redirect('log-in-department', userid = user.pk)
        # login(request, user)
        
        # if (group.name == "Engineer"):
        #   return redirect('log-in-department', userid = user.pk)
        
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
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'Company/login.html', {'form': form})

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

