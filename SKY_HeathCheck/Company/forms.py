from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from Company.models import Department, Session, Team

class CreateUserForm(UserCreationForm):
  
  group = forms.ModelChoiceField(Group.objects.all(), required = True)
  
  class Meta:
    model = User 
    fields = ['username', 'first_name', 'last_name', 'email']
    
class SelectDepartmentAndSession(forms.Form):
  department = forms.ModelChoiceField(queryset = Department.objects.all())
  team = forms.ModelChoiceField(queryset = Team.objects.none(), required = True)
  session = forms.ModelChoiceField(queryset = Session.objects.none(), required = True)
  
  
  def __init__(self, departmentID, teamID):
    department_id = departmentID.pop('department_id', None)
    super().__init__(self, departmentID, teamID)

    if department_id:
      self.fields['session'].queryset = Session.objects.filter(department_id=department_id)
      
    if department_id:
      self.fields['session'].queryset = Session.objects.filter(department_id=department_id)