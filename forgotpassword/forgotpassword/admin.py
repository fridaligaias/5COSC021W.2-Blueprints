from django.contrib import admin
from .models import (
    Department, 
    Team, 
    Session, 
    Account, 
    SessionCard, 
    Vote, 
    Card, 
    CardToDepartment
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('departmentID', 'departmentName')
    search_fields = ['departmentName']

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
    list_display = ('accountCode', 'name', 'userName', 'password', 'emailAddress', 'accountRole', 'departmentID')
    list_filter = ['accountRole', 'departmentID']
    search_fields = ['name', 'userName', 'emailAddress']

@admin.register(SessionCard)
class SessionCardAdmin(admin.ModelAdmin):
    list_display = ('sessionCardID', 'sessionID', 'greenVote', 'amberVote', 'redVote')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voteCode', 'sessionCardID', 'accountCode', 'greenVote', 'amberVote', 'redVote')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('cardID', 'greenDescription', 'amberDescription', 'redDescription')

@admin.register(CardToDepartment)
class CardToDepartmentAdmin(admin.ModelAdmin):
    list_display = ('cardID', 'departmentID')