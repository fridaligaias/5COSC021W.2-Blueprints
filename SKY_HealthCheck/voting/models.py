from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Session(models.Model):
    name = models.CharField(max_length=100)

class Team(models.Model):
    name = models.CharField(max_length=100)

class HealthCard(models.Model):
    title = models.CharField(max_length=200)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    health_card = models.ForeignKey(HealthCard, on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        unique_together = ('user', 'health_card')
