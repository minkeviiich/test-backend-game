from django.db import models
from django.contrib.auth.models import User
import csv
from django.http import HttpResponse
from django.utils import timezone


class Player(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
    )
    first_login = models.DateTimeField(
        null=True, 
        blank=True
    )
    daily_points = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.user.username
    
    def assign_prize(self, level, prize, boost=None):
        player_level, created = PlayerLevel.objects.get_or_create(
            player=self, 
            level=level
        )
        if not player_level.is_completed:
            player_level.is_completed = True
            player_level.save()
            LevelPrize.objects.create(
                level=level, 
                prize=prize, 
                received=timezone.now(), 
                boost=boost
            ) 


class Boost(models.Model):
    name = models.CharField(
        max_length=100
    )
    description = models.TextField()

    def __str__(self):
        return self.name


class Level(models.Model):
    title = models.CharField(
        max_length=100
    )
    order = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.title


class Prize(models.Model):
    title = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.title


class PlayerLevel(models.Model):
    player = models.ForeignKey(
        Player, 
        on_delete=models.CASCADE
    )
    level = models.ForeignKey(
        Level, 
        on_delete=models.CASCADE
    )
    completed = models.DateField()
    is_completed = models.BooleanField(
        default=False
    )
    score = models.PositiveIntegerField(
        default=0
    )


class LevelPrize(models.Model):
    level = models.ForeignKey(
        Level, 
        on_delete=models.CASCADE
    )
    prize = models.ForeignKey(
        Prize, 
        on_delete=models.CASCADE
    )
    received = models.DateField()
    boost = models.ForeignKey(
        Boost, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
