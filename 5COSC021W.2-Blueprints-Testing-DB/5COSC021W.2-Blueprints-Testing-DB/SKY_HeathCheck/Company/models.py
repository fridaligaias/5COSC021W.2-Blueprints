from django.db import models

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
  
class Department(models.Model):
  departmentID = models.AutoField(primary_key = True, unique = True)
  departmentName = models.CharField(max_length = 200, null = True)  
  
  def __str__(self):
    return f"ID : {self.departmentID} | {self.departmentName}"
  
class Team(models.Model):
  departmentID = models.ForeignKey(Department, on_delete = models.CASCADE)
  teamID = models.AutoField(primary_key = True, unique = True)
  teamName = models.CharField(max_length = 200, default = "")
  
  def __str__(self):
    return f"ID : {self.teamID} | {self.teamName} [{self.departmentID.departmentName}]"
  
class Session(models.Model):
  teamID = models.ForeignKey(Team, on_delete = models.CASCADE)
  sessionID = models.AutoField(primary_key = True, unique = True)
  
  sessionName = models.CharField(max_length = 200, default = "New Session")
  sessionStartData = models.DateTimeField(editable = True)
  sessionEndData = models.DateTimeField(editable = True)
  
  def __str__(self):
    return f"ID : {self.sessionID} | {self.sessionName} [{self.teamID.teamName}] > Start: {self.sessionStartData.date()} ~ End: {self.sessionEndData.date()}"

class Account(models.Model):
  ENGINEER = "ENGINEER"
  TEAM_LEADER = "TEAM LEADER"
  DEPARTMENT_LEADER = "DEPARTMENT LEADER"
  SENIOR_MANAGER = "SENIOR MANAGER"
  
  EmployeeType = {
    ENGINEER : "ENGINEER",
    TEAM_LEADER : "TEAM LEADER",
    DEPARTMENT_LEADER : "DEPARTMENT LEADER",
    SENIOR_MANAGER : "SENIOR MANAGER",
  }
  
  userID = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
  departmentID = models.ForeignKey(Department, on_delete = models.CASCADE, default = "")
  accountCode = models.AutoField(primary_key = True, unique = True)
  name = models.CharField(max_length = 200, default = "")
  userName = models.CharField(max_length = 200, default = "")
  emailAddress = models.EmailField(max_length = 254)
  password = models.CharField(max_length = 254)
  password = models.CharField(max_length = 254)
  accountRole = models.CharField(max_length = 20, choices = EmployeeType, default = ENGINEER)
  
  def __str__(self):
    return f"ID : {self.accountCode} | {self.name}"
  
class SessionCard(models.Model):
  sessionID = models.ForeignKey(Session, on_delete = models.CASCADE)
  sessionCardID = models.AutoField(primary_key = True)
  greenVote = models.IntegerField(default = 0)
  amberVote = models.IntegerField(default = 0)
  redVote = models.IntegerField(default = 0)
  greenDescription = models.CharField(max_length = 500, default = "" )
  amberDescription = models.CharField(max_length = 500, default = "" )
  redDescription = models.CharField(max_length = 500, default = "" )
  
class Vote(models.Model):
  sessionCardID = models.ForeignKey(SessionCard, on_delete = models.CASCADE)
  accountCode = models.ForeignKey(Account, on_delete = models.CASCADE)
  voteCode = models.AutoField(primary_key = True, unique = True)
  greenVote = models.BooleanField(default = False)
  amberVote = models.BooleanField(default = False)
  redVote = models.BooleanField(default = False)
  comment = models.CharField(max_length = 500)
  
  
  
  
class Card(models.Model):
    cardID = models.AutoField(primary_key=True)
    greenDescription = models.TextField(max_length=500) 
    amberDescription = models.TextField(max_length=500)
    redDescription = models.TextField(max_length=500)    
    
    def __str__(self):
        return f"Card {self.cardID}"
      
      
class CardToDepartment(models.Model):
    cardID = models.ForeignKey(Card, on_delete=models.CASCADE)
    departmentID = models.ForeignKey('Department', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('cardID', 'departmentID')