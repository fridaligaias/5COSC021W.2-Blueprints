from django.contrib import admin

from Company.models import *

##SECTION - 
# Members on site:
# (Siu Kitt, Dat):
admin.site.register(Account)
admin.site.register(Department)
admin.site.register(Team)
admin.site.register(Session)
admin.site.register(Card)
admin.site.register(Vote)
admin.site.register(SessionCard)
