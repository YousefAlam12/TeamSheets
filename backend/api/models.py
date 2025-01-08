from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.gis.db import models
from datetime import date

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    date_of_birth = models.DateField()

class Game(models.Model):
    # location = models.PointField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(null=True)
    price = models.FloatField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_games')

    def __str__(self):
        return f"Game {self.id} admined by {self.admin.username}"