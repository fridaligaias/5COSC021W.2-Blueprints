from django.db import models

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
  
class Card(models.Model):
  # main ID for the card model
  cardID = models.CharField(primary_key = True, unique = True, max_length = 20)
  # contains the image for a specific card 
  cardImage = models.ImageField(upload_to = 'cards/', null = True)
  # holds all of the descriptions for each of the cards, from red to green
  greenDescription = models.TextField(max_length = 150) 
  amberDescription = models.TextField(max_length = 150)
  redDescription = models.TextField(max_length = 150)    
    
  # only visible for the admin view - what they see when a new card is made
  def __str__(self):
    return f"Card : {self.cardID}"
  
class Department(models.Model):
  # main ID
  departmentID = models.AutoField(primary_key = True, unique = True)
  # the name
  departmentName = models.CharField(max_length = 200, null = True)  
  # Allows for the admin to select a specific number of cards a department could have if they make a session
  departmentCards = models.ManyToManyField(Card)
  
  # only visible for the admin view - what they see when a new card is made  
  def __str__(self):
    return f"ID : {self.departmentID} | {self.departmentName}"
  
class Team(models.Model):
  # foreign key to the department to link their relationship
  departmentID = models.ForeignKey(Department, on_delete = models.CASCADE)
  # main ID
  teamID = models.AutoField(primary_key = True, unique = True)
  teamName = models.CharField(max_length = 200, default = "")
  
  # only visible for the admin view - what they see when a new card is made
  def __str__(self):
    return f"ID : {self.teamID} | {self.teamName} [{self.departmentID.departmentName}]"
  
class Session(models.Model):
  # links the session to a specific team that made it 
  teamID = models.ForeignKey(Team, on_delete = models.CASCADE)
  # id for the session
  sessionID = models.AutoField(primary_key = True, unique = True)
  
  # some basic meta data for the sessions like time and name
  sessionName = models.CharField(max_length = 200, default = "New Session")
  sessionStartData = models.DateTimeField(editable = True)
  sessionEndData = models.DateTimeField(editable = True)
  
  # only visible for the admin view - what they see when a new card is made
  def __str__(self):
    return f"ID : {self.sessionID} | {self.sessionName} [{self.teamID.teamName}] > Start: {self.sessionStartData.date()} ~ End: {self.sessionEndData.date()}"
  
class Account(models.Model):
  # links the user to the rest of the mainframe
  accountID = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
  # links the account to the center of origin
  departmentID = models.ForeignKey(Department, on_delete = models.CASCADE, null = True)
  
  # only visible for the admin view - what they see when a new card is made
  def __str__(self):
    return f"ID : {self.accountID} | {self.accountID.first_name} {self.accountID.last_name}"

class SessionCard(models.Model):
  # different to cards as this is what the user will specific vote from and add up to
  
  # links to the specific session the card is from
  sessionID = models.ForeignKey(Session, on_delete = models.CASCADE)
  # main ID
  sessionCardID = models.AutoField(primary_key = True, unique = True)
  # basic meta for the cards like images and the number of votes from members
  cardImage = models.ImageField(upload_to = 'cards/', null = True)
  greenVote = models.IntegerField(default = 0)
  amberVote = models.IntegerField(default = 0)
  redVote = models.IntegerField(default = 0)
  # basic description that was made from the cards
  greenDescription = models.CharField(max_length = 150, default = "")
  amberDescription = models.CharField(max_length = 150, default = "")
  redDescription = models.CharField(max_length = 150, default = "")
  
  # only visible for the admin view - what they see when a new card is made
  def __str__(self):
    return f"Team : {self.sessionID.sessionName} | {self.sessionCardID}"
  
class Vote(models.Model):
  # handles the individual storing of a user's vote
  
  # links from the session card to make sure which vote is from where
  sessionCardID = models.ForeignKey(SessionCard, on_delete = models.CASCADE)
  # which users the specific vote is from
  userID = models.ForeignKey(User, on_delete = models.CASCADE)
  # main ID
  voteCode = models.AutoField(primary_key = True, unique = True)
  # basic meta data
  greenVote = models.IntegerField(default = 0)
  amberVote = models.IntegerField(default = 0)
  redVote = models.IntegerField(default = 0)
  comment = models.CharField(max_length = 200)
  
@receiver(post_save, sender = Session)
# auto creates the sessions cards which a session is made
def SetSessionCards(sender, instance, created, **kwargs):
    department = instance.teamID.departmentID.departmentCards.all()
    SessionCard.objects.bulk_create([SessionCard(sessionID = instance, 
                                                 cardImage = card.cardImage,
                                                 greenDescription = card.greenDescription,
                                                 amberDescription = card.amberDescription,
                                                 redDescription = card.redDescription) for card in department])
# auto creates the account when a new user is made
@receiver(post_save, sender = User)
def SetAccountUser(sender, instance, created, **kwargs):
  if (created): Account.objects.create(accountID = instance)
  
  
   
  