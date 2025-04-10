from django.db import models

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
  
class Card(models.Model):
  cardID = models.CharField(primary_key = True, unique = True, max_length = 20)
  greenDescription = models.TextField(max_length = 150) 
  amberDescription = models.TextField(max_length = 150)
  redDescription = models.TextField(max_length = 150)    
    
  def __str__(self):
    return f"Card : {self.cardID}"
  
class Department(models.Model):
  departmentID = models.AutoField(primary_key = True, unique = True)
  departmentName = models.CharField(max_length = 200, null = True)  
  departmentCards = models.ManyToManyField(Card)
  
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

  accountID = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
  departmentID = models.ForeignKey(Department, on_delete = models.CASCADE, default = "")
  
  def __str__(self):
    return f"ID : {self.accountID} | {self.accountID.first_name} {self.accountID.last_name}"

class SessionCard(models.Model):
  sessionID = models.ForeignKey(Session, on_delete = models.CASCADE)
  
  sessionCardID = models.AutoField(primary_key = True, unique = True)
  greenVote = models.IntegerField(default = 0)
  amberVote = models.IntegerField(default = 0)
  redVote = models.IntegerField(default = 0)
  
  greenDescription = models.CharField(max_length = 500, default = "")
  amberDescription = models.CharField(max_length = 500, default = "")
  redDescription = models.CharField(max_length = 500, default = "")
  
  def __str__(self):
    return f"Team : {self.sessionID.sessionName} | {self.sessionCardID}"
  
class Vote(models.Model):
  sessionCardID = models.ForeignKey(SessionCard, on_delete = models.CASCADE)
  userID = models.ForeignKey(User, on_delete = models.CASCADE)
  voteCode = models.AutoField(primary_key = True, unique = True)
  greenVote = models.IntegerField(default = 0)
  amberVote = models.IntegerField(default = 0)
  redVote = models.IntegerField(default = 0)
  
  comment = models.CharField(max_length = 200)
  
@receiver(post_save, sender = Session)
def SetSessionCards(sender, instance : Session, created, **kwargs):
    department = instance.teamID.departmentID.departmentCards.all()
    SessionCard.objects.bulk_create([SessionCard(sessionID = instance, 
                                                 greenDescription = card.greenDescription,
                                                 amberDescription = card.amberDescription,
                                                 redDescription = card.redDescription) for card in department])
  
  
   
  