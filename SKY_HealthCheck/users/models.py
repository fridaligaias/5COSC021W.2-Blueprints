from django.db import models

class User(models.Model):
    # Your model fields here
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    # Add other fields as needed
