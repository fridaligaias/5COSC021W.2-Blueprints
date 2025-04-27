from django.contrib import admin

from skyhealthcheckapp.models import *


# Register your models here.
admin.site.register(Account)
admin.site.register(Department)
admin.site.register(Team)
admin.site.register(Session)
admin.site.register(Card)
admin.site.register(Vote)
admin.site.register(SessionCard)
