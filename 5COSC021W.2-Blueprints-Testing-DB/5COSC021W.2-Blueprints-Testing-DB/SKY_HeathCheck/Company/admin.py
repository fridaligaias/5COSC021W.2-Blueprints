from django.contrib import admin

from Company.models import Account, Department, Session, Team, SessionCard, CardToDepartment, Card, Vote

# Register your models here.

admin.site.register(Account)
admin.site.register(Department)
admin.site.register(Team)
admin.site.register(Session)
admin.site.register(SessionCard)    
admin.site.register(Card)
admin.site.register(Vote)
admin.site.register(CardToDepartment)
