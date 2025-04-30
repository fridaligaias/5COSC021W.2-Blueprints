from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from Company.models import Department, Session, Team
from django.core.exceptions import ValidationError
from django.db.models import Q

##SECTION - 
# Members on site:
# (Siu Kitt, Dat):

class CreateUserForm(UserCreationForm):
  # gathers all of the groups into a dropdwon
  group = forms.ModelChoiceField(Group.objects.all(), required = True)
  # all of the necessary fields we'd like
  class Meta:
    model = User 
    fields = ['username', 'first_name', 'last_name', 'email']

# get all of the departments
class SelectDepartment(forms.Form):
  department = forms.ModelChoiceField(Department.objects.all(), required = True)

# get all of the team
class SelectTeam(forms.Form):
  team = forms.ModelChoiceField(queryset = Team.objects.none(), required = True)
  
  def __init__(self, *args, **kwargs):
    # get the department id and filter the teams based
    departmentID = kwargs.pop('departmentID', None) 
    super().__init__(*args, **kwargs)

    if departmentID:
      self.fields['team'].queryset = Team.objects.filter(departmentID = departmentID)
    else:
      self.fields['team'].queryset = Team.objects.none()

# get all of the sessions
class SelectSession(forms.Form):
  session = forms.ModelChoiceField(queryset = Session.objects.none(), required = True)
  
  # get the team id and filter all of the sessions based
  def __init__(self, *args, **kwargs):
    teamID = kwargs.pop('teamID', None) 
    super().__init__(*args, **kwargs)

    if teamID:
      self.fields['session'].queryset = Session.objects.filter(teamID = teamID)
    else:
      self.fields['session'].queryset = Session.objects.none()
    
# create the form we need        
class VotingForm(forms.Form):
  # hide the id for the sessions
  session_card_id = forms.IntegerField(widget = forms.HiddenInput())
  # create the fields for the radio inputs
  vote_type = forms.ChoiceField(choices = [
    ('green', 'Green'),
    ('amber', 'Amber'),
    ('red', 'Red')
  ], widget = forms.RadioSelect)
  # create the input box
  comment = forms.CharField(
    max_length = 200, 
    required = True, 
    widget = forms.Textarea(attrs = {'rows': 10, 
                                     'cols': 40,
                                     'style': 'resize: none;',
                                     'placeholder': 'Optional comment...'})
)
  
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