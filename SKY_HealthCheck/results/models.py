from django.db import models

class VoteSummary(models.Model):
    session = models.ForeignKey('voting.Session', on_delete=models.CASCADE)
    total_votes = models.IntegerField()
    # Add other summary fields
