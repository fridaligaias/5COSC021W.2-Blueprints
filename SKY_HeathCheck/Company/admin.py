from django.contrib import admin

from Company.models import Account, Department, Session, Team

# Register your models here.
admin.site.register(Account)
admin.site.register(Department)
admin.site.register(Team)
admin.site.register(Session)
