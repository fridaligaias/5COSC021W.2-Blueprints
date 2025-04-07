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
  
   
  