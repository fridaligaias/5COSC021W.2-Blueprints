from django.contrib import admin

from Company.models import Department, Session, Team

# Register your models here.
admin.site.register(Department)
admin.site.register(Team)
admin.site.register(Session)
