from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from Company.models import Department, Session, Team

class CreateUserForm(UserCreationForm):
  
  group = forms.ModelChoiceField(Group.objects.all(), required = True)
  
  class Meta:
    model = User 
    fields = ['username', 'first_name', 'last_name', 'email']
    
class SelectDepartment(forms.Form):
  department = forms.ModelChoiceField(Department.objects.all(), required = True)
  
class SelectTeam(forms.Form):
  team = forms.ModelChoiceField(queryset = Team.objects.none(), required = True)
  
  def __init__(self, *args, **kwargs):
          departmentID = kwargs.pop('departmentID', None)  # Get passed departmentID
          super().__init__(*args, **kwargs)

          if departmentID:
              self.fields['team'].queryset = Team.objects.filter(departmentID = departmentID)
          else:
              self.fields['team'].queryset = Team.objects.none()
  
class SelectSession(forms.Form):
  session = forms.ModelChoiceField(queryset = Session.objects.none(), required = True)
  
  def __init__(self, *args, **kwargs):
          teamID = kwargs.pop('teamID', None)  # Get passed team_id
          super().__init__(*args, **kwargs)

          if teamID:
              self.fields['session'].queryset = Session.objects.filter(teamID = teamID)
          else:
              self.fields['session'].queryset = Session.objects.none()
              
class VotingForm(forms.Form):
  session_card_id = forms.IntegerField(widget = forms.HiddenInput())
  vote_type = forms.ChoiceField(choices = [
    ('green', 'Green'),
    ('amber', 'Amber'),
    ('red', 'Red')
  ], widget = forms.RadioSelect)
  comment = forms.CharField(
    max_length = 200, 
    required = True, 
    widget = forms.Textarea(attrs = {'rows': 10, 
                                     'cols': 40,
                                     'style': 'resize: none;',
                                     'placeholder': 'Optional comment...'})
)