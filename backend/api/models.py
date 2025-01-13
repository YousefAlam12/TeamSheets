from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from datetime import date, time

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    date_of_birth = models.DateField()


class Game(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(null=True)
    totalPlayers = models.IntegerField()
    price = models.FloatField()
    address = models.CharField(max_length=100)
    postcode = models.CharField(max_length=50)
    location = models.PointField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_games')
    players = models.ManyToManyField(User, through='Player')

    def __str__(self):
        return f"Game {self.id}"


    def as_dict(self):
        start_time = self.start_time.strftime('%H:%M')
        end_time = self.end_time.strftime('%H:%M')

        return {
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'start_time': start_time,
            'end_time': end_time,
            'description': self.description,
            'totalPlayers': self.totalPlayers,
            'price': self.price,
            'address': self.address,
            'postcode': self.postcode,
            'location': self.location.coords,  # Extract coordinates if location is a PointField
            'admin': {
                'id': self.admin.id,
                'username': self.admin.username
            },
            'players': [
                {
                    'id': player.id,
                    'username': player.username
                } for player in self.players.all()
            ]  # List of dictionaries for each player with id and username
        }


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

    
    def as_dict(self):
        return {
            'id': self.id,
            'user': {
                'id': self.user.id,
                'username': self.user.username
            },
            'game': self.game.id,
            'paid': self.paid,
            'team': self.team
        }
