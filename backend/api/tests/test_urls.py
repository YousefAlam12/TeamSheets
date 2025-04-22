from django.test import TestCase
from django.urls import reverse, resolve
import api.views as views
from api import models
from datetime import date, time, timedelta
from django.utils import timezone
from django.contrib.gis.geos import Point


class TestUrls(TestCase):
    def setUp(self):
        # test user
        self.user1 = models.User.objects.create_user(
            first_name="user1", last_name="testing", username="user1", password="password1", email="user1@email.com", date_of_birth=date(2000, 1, 1), postcode="IG11 9BX", location=Point(0.105618, 51.549457)
        )

        d = date(2027, 8, 22)
        start_t = time(12, 00)
        end_t = time(14, 00)
        # test game
        self.game1 = models.Game.objects.create(name="Game 1", date=d, start_time=start_t, end_date=d, end_time=end_t, totalPlayers=10, price=5, address="Fairlop Oaks Playing Fields, Forest Rd, Ilford", postcode="IG6 3HX", location=Point(0.100324, 51.598645), admin=self.user1, is_private=False, fulltime=False)


    def test_url_login(self):
        url = reverse("Login")
        self.assertEqual(resolve(url).func, views.login_api)


    def test_url_logout(self):
        url = reverse("Logout")
        self.assertEqual(resolve(url).func, views.logout_api)


    def test_url_signup(self):
        url = reverse("Signup")
        self.assertEqual(resolve(url).func, views.signup)

    
    def test_url_isAuthenticated(self):
        url = reverse("isAuthenticated")
        self.assertEqual(resolve(url).func, views.isAuthenticated)


    def test_url_sendFriendRequest(self):
        url = reverse("Send Friend Request")
        self.assertEqual(resolve(url).func, views.send_friend_request)

    
    def test_url_friends(self):
        url = reverse("Friends")
        self.assertEqual(resolve(url).func, views.friends_api)


    def test_url_profile(self):
        url = reverse("Profile")
        self.assertEqual(resolve(url).func, views.profile_api)


    def test_url_password(self):
        url = reverse("Password")
        self.assertEqual(resolve(url).func, views.password_api)


    def test_url_myGames(self):
        url = reverse("My Games")
        self.assertEqual(resolve(url).func, views.my_games_api)


    def test_url_games(self):
        url = reverse("Games")
        self.assertEqual(resolve(url).func, views.games_api)


    def test_url_game(self):
        url = reverse("Game_api", args=[1])
        self.assertEqual(resolve(url).func, views.game_api)


    def test_url_teams(self):
        url = reverse("Teams", args=[1])
        self.assertEqual(resolve(url).func, views.teams_api)


    def test_url_balanceTeam(self):
        url = reverse("Balance Teams", args=[1])
        self.assertEqual(resolve(url).func, views.balanceTeams)


    def test_url_ratings(self):
        url = reverse("Ratings", args=[1])
        self.assertEqual(resolve(url).func, views.ratings_api)

    
    def test_url_gameInvite(self):
        url = reverse("Game Invite", args=[1])
        self.assertEqual(resolve(url).func, views.gameInvite)

    
    def test_url_matchmake(self):
        url = reverse("Matchmake")
        self.assertEqual(resolve(url).func, views.matchmake_api)