from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from datetime import date, time

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    date_of_birth = models.DateField()
    postcode = models.CharField(max_length=50)
    location = models.PointField()
    friends = models.ManyToManyField("User", blank=True)

    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'stats': self.stats,
            'friends': [
                {'id': friend.id, 'username': friend.username, 'stats': friend.stats}
                for friend in self.friends.all()
            ],
            'sent_requests': [
                {'id': to_user_id, 'username': to_user_username}
                for to_user_id, to_user_username in self.from_user.all().values_list('to_user__id', 'to_user__username')
            ],
            'received_requests': [
                {'id': req.from_user.id, 'username': req.from_user.username, 'stats': req.from_user.stats}
                # for from_user_id, from_user_username in self.to_user.all().values_list('from_user__id', 'from_user__username')
                for req in self.to_user.all()
            ],
            'game_invites': [
                inv.as_dict()
                for inv in self.invite_to.all()
            ],
            'subscribed_games': [
                notif.as_dict()
                for notif in self.subscribed_games.all()
            ]
        }

    @property
    def stats(self):
        ratings = self.ratings.all()

        if len(ratings) <= 0:
            return None

        stats = {
            'attack': 0,
            'defence': 0,
            'strength': 0,
            'speed': 0,
            'technique': 0
        }

        for r in ratings:
            stats['attack'] += r.attack
            stats['defence'] += r.defence
            stats['strength'] += r.strength
            stats['speed'] += r.speed
            stats['technique'] += r.technique

        for s in stats:
            stats[s] = round(stats[s] / len(ratings), 1)

        return stats
    
    @property
    # overall rating used to apply skill based matchmaking on games
    def overallRating(self):
        # new users overall rating starts at 5
        if self.stats == None:
            return 5
        
        userRating = (self.stats['attack'] + self.stats['defence'] + self.stats['strength'] + self.stats['speed'] + self.stats['technique']) / 5
        userRating = round(userRating, 1)
        return userRating


class Game(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(null=True, blank=True)
    totalPlayers = models.IntegerField()
    price = models.FloatField()
    address = models.CharField(max_length=100)
    postcode = models.CharField(max_length=50)
    location = models.PointField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_games')
    players = models.ManyToManyField(User, through='Player')
    is_private = models.BooleanField(default=False)
    fulltime = models.BooleanField(default=False)

    def __str__(self):
        return f"Game {self.id}"

    def as_dict(self):
        start_time = self.start_time.strftime('%H:%M')
        end_time = self.end_time.strftime('%H:%M')

        players = Player.objects.filter(game=self).select_related('user')

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
            'location': self.location.coords,
            'is_private': self.is_private,
            'fulltime': self.fulltime,
            'admin': {
                'id': self.admin.id,
                'username': self.admin.username
            },
            'players': [
                {
                    'id': player.user.id,
                    'username': player.user.username,
                    'team': player.team,
                    'paid': player.paid,
                    'stats': player.user.stats
                } for player in players
            ]
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
            'game': self.game.id,
            'paid': self.paid,
            'team': self.team
        }


class Rating(models.Model):
    rater = models.ForeignKey(
        User, related_name="players_rated", on_delete=models.CASCADE)
    ratee = models.ForeignKey(
        User, related_name="ratings", on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    attack = models.FloatField()
    defence = models.FloatField()
    strength = models.FloatField()
    speed = models.FloatField()
    technique = models.FloatField()

    def __str__(self):
        return f"{self.rater} rated {self.ratee} for {self.game}"


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name="to_user", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.from_user} sent request to {self.to_user}"


class GameInvite(models.Model):
    from_user = models.ForeignKey(User, related_name="invite_from", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="invite_to", on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def as_dict(self):
        return {
            'id': self.id,
            'from_user': self.from_user.username,
            'game_id': self.game.id,
            'game_name': self.game.name,
        }

    def __str__(self):
        return f"{self.from_user} invited {self.to_user} to {self.game}"


class Notification(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="subscribed_games", on_delete=models.CASCADE)

    def as_dict(self):
        return {
            'game': self.game.id,
        }

    def __str__(self):
        return f"{self.user.username} is subscribed to {self.game} notifications"