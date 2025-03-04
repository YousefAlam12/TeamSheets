from django.contrib import admin
from api import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Game)
admin.site.register(models.Player)
admin.site.register(models.Rating)
admin.site.register(models.FriendRequest)
admin.site.register(models.GameInvite)
admin.site.register(models.Notification)