from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Driver(models.Model):

    name = models.CharField(max_length=30, null=True, blank=True)
    team = models.CharField(max_length=50, null=True, blank=True)
    teammate = models.CharField(max_length=30, null=True, blank=True)
    season_points = models.IntegerField()
    championships = models.IntegerField()
    wins = models.IntegerField()
