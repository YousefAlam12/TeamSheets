"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import test_api_view

from api import views


urlpatterns = [
    # API entry points should be defined here
    path('test', test_api_view, name='api test'),
    path('user', views.user_api, name='User'),
    path('login', views.login_api, name="Login"),
    path('logout', views.logout_api, name="Logout"),
    path('signup', views.signup, name="Signup"),
    path('isAuthenticated', views.isAuthenticated, name="isAuthenticated"),
    path('send_friend_request', views.send_friend_request, name="Send Friend Request"),
    path('friends', views.friends_api, name="Friends"),
    path('profile', views.profile_api, name="Profile"),
    path('password', views.password_api, name="Password"),

    path('allGames', views.all_games_api, name="All Games"),
    path('myGames', views.my_games_api, name="My Games"),
    path('games', views.games_api, name="Games"),
    path('game/<int:game_id>', views.game_api, name="Game_api"),
    path('teams/<int:game_id>', views.teams_api, name="Teams"),
    path('balanceTeams/<int:game_id>', views.balanceTeams, name="Balance Teams"),
    path('ratings/<int:game_id>', views.ratings_api, name="Ratings"),
    path('gameInvite/<int:game_id>', views.gameInvite, name="Game Invite"),
]
