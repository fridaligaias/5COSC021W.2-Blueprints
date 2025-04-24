from django.contrib import admin
from .models import (
    Department, 
    Team, 
    Session, 
    Account, 
    SessionCard, 
    Vote, 
    Card
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('departmentID', 'departmentName')
    search_fields = ['departmentName']
    filter_horizontal = ('departmentCards',)  # For the ManyToManyField

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('teamID', 'teamName', 'departmentID')
    list_filter = ['departmentID']
    search_fields = ['teamName']

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('sessionID', 'sessionName', 'teamID', 'sessionStartData', 'sessionEndData')
    list_filter = ['teamID', 'sessionStartData', 'sessionEndData']

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('accountID', 'get_username', 'get_full_name', 'get_email', 'departmentID')
    list_filter = ['departmentID']
    search_fields = ['accountID__username', 'accountID__first_name', 'accountID__last_name', 'accountID__email']
    
    def get_username(self, obj):
        return obj.accountID.username
    get_username.short_description = 'Username'
    
    def get_full_name(self, obj):
        return f"{obj.accountID.first_name} {obj.accountID.last_name}"
    get_full_name.short_description = 'Full Name'
    
    def get_email(self, obj):
        return obj.accountID.email
    get_email.short_description = 'Email'

@admin.register(SessionCard)
class SessionCardAdmin(admin.ModelAdmin):
    list_display = ('sessionCardID', 'sessionID', 'greenVote', 'amberVote', 'redVote')
    list_filter = ['sessionID']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voteCode', 'sessionCardID', 'userID', 'greenVote', 'amberVote', 'redVote')
    list_filter = ['sessionCardID', 'userID']

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('cardID', 'greenDescription', 'amberDescription', 'redDescription')
    search_fields = ['cardID', 'greenDescription', 'amberDescription', 'redDescription']