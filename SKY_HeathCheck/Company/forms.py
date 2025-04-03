from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
  
  class Meta:
    model = User 
    fields = ['username', 'first_name']
    
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    # self.fields['username'].help_text = '<small> Hello </small>'