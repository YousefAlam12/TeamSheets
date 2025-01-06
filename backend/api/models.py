from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    date_of_birth = models.DateField()