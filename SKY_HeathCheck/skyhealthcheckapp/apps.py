from django.apps import AppConfig
from django.contrib.auth.models import Group, User

class SkyhealthceckappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skyhealthcheckapp'

def ready(self):
        group_names = ['Admin', 'Senior Manager', 'Department Leader', 'Team Leader', 'Engineer']
        for group_name in group_names:
            Group.objects.get_or_create(name=group_name)
