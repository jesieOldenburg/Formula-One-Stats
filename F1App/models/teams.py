from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Teams(models.Model):
    
    team_name = models.CharField(max_length=75, null=True, blank=True)
    team_points = models.IntegerField()