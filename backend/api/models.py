from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from datetime import date

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    date_of_birth = models.DateField()


class Game(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(null=True)
    totalPlayers = models.IntegerField()
    price = models.FloatField()
    address = models.CharField(max_length=100)
    postcode = models.CharField(max_length=50)
    location = models.PointField()
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='admin_games')
    players = models.ManyToManyField(User, through='Player')

    def __str__(self):
        return f"Game {self.id}"


class Player(models.Model):
    TEAMS = [
        ('A', 'A'),
        ('B', 'B')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    team = models.CharField(max_length=1, choices=TEAMS, null=True, blank=True)

    def __str__(self):
        return f"{self.user} playing in {self.game}"
