from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = [
        ('engineer', 'Engineer'),
        ('leader', 'Leader'),
        ('manager', 'Manager'),
    ]
    role = models.CharField(max_length=10, choices=ROLES, default='engineer')
