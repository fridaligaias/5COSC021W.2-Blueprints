from django.db import models

# Declares the Account as a Django model
# region Account
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

  accountCode = models.AutoField(primary_key = True, unique = True)
  name = models.CharField(max_length = 20)
  userName = models.CharField(max_length = 20)
  emailAddress = models.EmailField(max_length = 254)
  password = models.CharField(('password'), max_length = 100)
  role = models.CharField(max_length = 20, choices = EmployeeType, default = "ENGINEER")

  class Meta:
    verbose_name = "Account"
    verbose_name_plural = "Accounts"

  def __str__(self):
    return f"ID ¦ {self.accountCode} | Name ¦ {self.name}"
# endregion

# Declares the Department as a Django model
# region Department
class Department(models.Model):


  class Meta:
    verbose_name = "Department"
    verbose_name_plural = "Departments"

  def __str__(self):
    return self.name

 # Declares the Team as a Django model
 # region Team
class Team(models.Model):


  class Meta:
    verbose_name = "Team"
    verbose_name_plural = "Teams"

  def __str__(self):
    return self.name

# Declares the Session as a Django model
# region Session
class Session(models.Model):


  class Meta:
    verbose_name = "Session"
    verbose_name_plural = "Sessions"

  def __str__(self):
    return self.name
