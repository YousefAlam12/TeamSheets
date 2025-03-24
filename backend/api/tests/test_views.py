from django.test import TestCase, Client
from api import models
import json
from django.urls import reverse
from datetime import date, time
from django.contrib.gis.geos import Point
from django.contrib.auth import authenticate

# NOTE: exceptions are thrown due to email notifications but this can be ignored as tests still work
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        # test users
        self.user1 = models.User.objects.create_user(
            first_name="user1", last_name="testing", username="user1", password="password1", email="user1@email.com", date_of_birth=date(2000, 1, 1), postcode="IG11 9BX", location=Point(0.105618, 51.549457)
        )
        self.user2 = models.User.objects.create_user(
            first_name="user2", last_name="testing", username="user2", password="password1", email="user2@email.com", date_of_birth=date(2000, 1, 1), postcode="IG11 9BX", location=Point(0.105618, 51.549457)
        )
        self.user3 = models.User.objects.create_user(
            first_name="user3", last_name="testing", username="user3", password="password1", email="user3@email.com", date_of_birth=date(2000, 1, 1), postcode="E1 0QE", location=Point(-0.045764, 51.515359)
        )

        # test games
        self.game1 = models.Game.objects.create(name="Game 1", date=date.today(), start_time=time(12, 0, 0), end_time=time(14, 0, 0), totalPlayers=10, price=5, address="Fairlop Oaks Playing Fields, Forest Rd, Ilford", postcode="IG6 3HX", location=Point(0.100324, 51.598645), admin=self.user1, is_private=False, fulltime=False)
        self.game2 = models.Game.objects.create(name="Game 2", date=date.today(), start_time=time(12, 0, 0), end_time=time(14, 0, 0), totalPlayers=10, price=5, address="Mile End Park Leisure Centre, Rhodeswell Rd, London", postcode="E3 4HL", location=Point(-0.031997, 51.519437), admin=self.user2, is_private=False, fulltime=False)
        self.privateGame = models.Game.objects.create(name="Game 2", date=date.today(), start_time=time(12, 0, 0), end_time=time(14, 0, 0), totalPlayers=10, price=5, address="Mile End Park Leisure Centre, Rhodeswell Rd, London", postcode="E3 4HL", location=Point(-0.031997, 51.519437), admin=self.user3, is_private=True, fulltime=False)
        self.fulltimeGame = models.Game.objects.create(name="Fulltime", date=date.today(), start_time=time(12, 0, 0), end_time=time(14, 0, 0), totalPlayers=10, price=5, address="Fairlop Oaks Playing Fields, Forest Rd, Ilford", postcode="IG6 3HX", location=Point(0.100324, 51.598645), admin=self.user2, is_private=False, fulltime=True)

        # GAME 1 test players
        models.Player.objects.create(user=self.user2, game=self.game1)

        # GAME 2 test players
        models.Player.objects.create(user=self.user1, game=self.game2)
        models.Player.objects.create(user=self.user2, game=self.game2)

        # FULLTIMEGAME test players
        models.Player.objects.create(user=self.user1, game=self.fulltimeGame)
        
        # PRIVATE GAME test players
        models.Player.objects.create(user=self.user1, game=self.privateGame)

        # Notification objects
        models.Notification.objects.create(game=self.game2, user=self.user1)
        


    def createPOST(self, url, data):
        response = self.client.post(url, data, content_type='application/json')
        return response
    
    def createDELETE(self, url, data):
        response = self.client.delete(url, data, content_type='application/json')
        return response
    
    def createPUT(self, url, data):
        response = self.client.put(url, data, content_type='application/json')
        return response


    def test_login(self):
        url = reverse("Login")

        # OK response on correct details
        response = self.createPOST(url, {'username': 'user1', 'password': 'password1'})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        # BAD response on incorrect details
        response = self.createPOST(url, {'username': 'user1', 'password': 'pass'})
        self.assertEqual(response.status_code, 400)


    def test_logout(self):
        self.client.login(username="user1", password="password1")
        response = self.client.get(reverse('Logout'))
        self.assertEqual(response.status_code, 200)

    
    def test_signup(self):
        url = reverse('Signup')
        response = self.createPOST(url, {
            'firstname': "test",
            'lastname': "testing", 
            'email': "new@email.com", 
            'dob': date(2000, 1, 1), 
            'postcode': "IG11 9BX", 
            'longitude': 0.105618,
            'latitude': 51.549457,
            'username': "newUser", 
            'password1': "test1234", 
            'password2': "test1234", 
        })
        newUser = models.User.objects.filter(username="newUser")

        # check user was created
        self.assertEqual(len(newUser), 1)
        self.assertEqual(response.status_code, 200)

    
    def test_authentication(self):
        url = reverse('isAuthenticated')

        # check true returns when logged in
        self.client.login(username="user1", password="password1")
        response = self.client.get(url)
        res = response.json()
        self.assertEqual(res['isAuth'], True)
        self.client.logout()

        # check false returns when logged out 
        response = self.client.get(url)
        res = response.json()
        self.assertEqual(res['isAuth'], False)

    
    def test_sendFriendRequest(self):
        self.client.login(username="user1", password="password1")
        url = reverse('Send Friend Request')
        response = self.createPOST(url, {'to_user' : 2})
        res = response.json()

        # should return user as dictionary
        self.assertIsNotNone(res.get('user'))

        # check if sent request is in user dictionary
        self.assertEqual(len(res['user']['sent_requests']), 1)

        # FriendRequest object should be created
        friend_requests = models.FriendRequest.objects.all()
        self.assertEqual(len(friend_requests), 1)


    def test_friends_GET(self):
        url = reverse('Friends')
        self.client.login(username="user1", password="password1")
        response = self.client.get(url)
        res = response.json()

        # should return response with list of all users and user as dictionary
        self.assertIsNotNone(res.get('user'))
        self.assertGreaterEqual(len(res.get('userList')), 1)


    def test_friends_Accept(self):
        url = reverse('Friends')
        
        # user 1 send friend request to user 2
        self.client.login(username="user1", password="password1")
        response = self.createPOST(reverse('Send Friend Request'), {'to_user' : 2})
        self.client.logout()

        # login as user 2 and accept request
        self.client.login(username="user2", password="password1")
        response = self.client.get(url)
        res = response.json()

        # user dictionary should contain friend request in received_requests
        self.assertEqual(len(res['user']['received_requests']), 1)

        # accept friend request
        from_user = res['user']['received_requests'][0].get('id')
        response  = self.createPOST(url, {'from_user': from_user})
        res = response.json()

        # checks if sending user is added to friends and vice versa 
        self.assertEqual(len(res['user']['friends']), 1)
        self.assertEqual(len(self.user2.friends.all()), 1)
        self.assertEqual(len(self.user1.friends.all()), 1)

        # FriendRequest object should be deleted
        friend_requests = models.FriendRequest.objects.all()
        self.assertEqual(len(friend_requests), 0)


    def test_friends_Reject(self):
        url = reverse('Friends')
    
        # user 1 send friend request to user 2
        self.client.login(username="user1", password="password1")
        response = self.createPOST(reverse('Send Friend Request'), {'to_user' : 2})
        self.client.logout()

        # login as user 2 and reject request
        self.client.login(username="user2", password="password1")
        response = self.client.get(url)
        res = response.json()

        # user dictionary should contain friend request in received_requests
        self.assertEqual(len(res['user']['received_requests']), 1)

        # reject friend request
        from_user = res['user']['received_requests'][0].get('id')
        response  = self.createDELETE(url, {'from_user': from_user})
        res = response.json()

        # checks if sending user has not added to friends and vice versa 
        self.assertEqual(len(res['user']['friends']), 0)
        self.assertEqual(len(self.user2.friends.all()), 0)
        self.assertEqual(len(self.user1.friends.all()), 0)

        # FriendRequest object should be deleted
        friend_requests = models.FriendRequest.objects.all()
        self.assertEqual(len(friend_requests), 0)
    

    def test_profile(self):
        url = reverse('Profile')

        self.client.login(username="user1", password="password1")
        response = self.createPUT(url, {
            'email': "change@email.com",
            'longitude': -0.045764,
            'latitude': 51.515359,
            'postcode': "E1 0QE",
        })
        res = response.json()

        self.assertEqual(response.status_code, 200)
        self.client.logout()
        user1 = models.User.objects.get(id=1)

        self.assertEqual(user1.email, "change@email.com")
        self.assertEqual(user1.postcode, "E1 0QE")
        self.assertEqual(user1.location.x, -0.045764)
        self.assertEqual(user1.location.y, 51.515359)
        

    def test_password(self):
        url = reverse("Password")
        self.client.login(username="user1", password="password1")
        
        # check valid case
        response = self.createPUT(url, {
            'old': "password1",
            'new': "newpassword"
        })
        changed = authenticate(username="user1", password="newpassword")

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(changed)

        # check invalid case
        response = self.createPUT(url, {
            'old': "pass",
            'new': "invalid"
        })
        changed = authenticate(username="user1", password="invalid")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(changed, None)
    

    def test_mygames(self):
        url = reverse("My Games")
        self.client.login(username="user1", password="password1")

        response = self.client.get(url)
        res = response.json()

        self.assertEqual(len(res['myGames']), 2)
        self.assertEqual(len(res['adminGames']), 1)
        self.assertEqual(len(res['playedGames']), 1)


    def test_games_GET(self):
        url = reverse("Games")
        self.client.login(username="user1", password="password1")
        response = self.client.get(url)
        res = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res['games']), 2)


    def test_games_POST(self):
        url = reverse("Games")
        self.client.login(username="user1", password="password1")
    
        response = self.createPOST(url, {
            'game' : {
                'name': "Test Game",
                'date': date.today(),
                'start_time': "12:00",
                'end_time': "14:00",
                'description': "testing 123.......",
                'totalPlayers': 10,
                'price': 5,
                'address': "Fairlop Oaks Playing Fields, Forest Rd, Ilford",
                'postcode': "IG6 3HX",
                'longitude': 0.100324,
                'latitude': 51.598645,
                'is_private': False
            }
        })
        
        # check if game was created and admin is a player
        testGame = models.Game.objects.filter(name="Test Game")
        player = models.Player.objects.filter(game=testGame[0])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(testGame), 1)
        self.assertEqual(len(player), 1)


    def test_game_GET(self):
        self.client.login(username="user1", password="password1")

        # check for game that exists
        url = reverse("Game_api", args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        
        # check for game that does not exist
        url = reverse("Game_api", args=[100])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)

        # only admin and players should be able to view private game
        url = reverse("Game_api", args=[3])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.client.logout()
        self.client.login(username="user3", password="password1")
        url = reverse("Game_api", args=[3])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # user who is not player or admin of game should not be able to view
        self.client.logout()
        self.client.login(username="user2", password="password1")
        url = reverse("Game_api", args=[3])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)


    def test_game_POST(self):
        url = reverse("Game_api", args=[1])
        self.client.login(username="user3", password="password1")

        response = self.createPOST(url, {'join' : True})
        player = models.Player.objects.filter(game=1, user=3)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(player), 1)


    # DELETE methods for game_api
    def test_game_LEAVE(self):
        url = reverse("Game_api", args=[2])
        self.client.login(username="user1", password="password1")

        response = self.createDELETE(url, {'leave' : True})
        player = models.Player.objects.filter(game=1, user=1)
        notification = models.Notification.objects.filter(game=1, user=1)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(player), 0)
        self.assertEqual(len(notification), 0)

    
    def test_game_KICK(self):
        url = reverse("Game_api", args=[2])
        self.client.login(username="user2", password="password1")

        response = self.createDELETE(url, {'kick' : 1})
        player = models.Player.objects.filter(game=2, user=1)
        notification = models.Notification.objects.filter(game=1, user=1)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(player), 0)
        self.assertEqual(len(notification), 0)


    def test_game_CANCEL(self):
        url = reverse("Game_api", args=[1])
        self.client.login(username="user1", password="password1")

        response = self.createDELETE(url, {'cancel_game' : True})
        game = models.Game.objects.filter(id=1)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(game), 0)

    
    def test_game_UNSUBSCRIBE(self):
        url = reverse("Game_api", args=[2])
        self.client.login(username="user1", password="password1")

        response = self.createDELETE(url, {'unsubscribe' : True})
        notification = models.Notification.objects.filter(id=2)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(notification), 0)


    # tests all PUT methods in game_api
    def test_game_PUT(self):
        # url is game where user is admin and bad_url is where it is not
        url = reverse("Game_api", args=[2])
        bad_url = reverse("Game_api", args=[1])
        self.client.login(username="user2", password="password1")

        # checks player paid status changes
        response = self.createPUT(url, {'paid': True})
        player = models.Player.objects.get(game=2, user=2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(player.paid, True)

        # checks game privacy changes (only admin)
        response = self.createPUT(url, {'toggle_privacy': True})
        bad_response = self.createPUT(bad_url, {'toggle_privacy': True})
        game = models.Game.objects.get(id=2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bad_response.status_code, 400)
        self.assertEqual(game.is_private, True)

        # checks if notification object is created when user subscribes
        response = self.createPUT(url, {'subscribe': True})
        notification = models.Notification.objects.filter(game=game, user=2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(notification), 1)

        # checks game is set to fulltime (only admin)
        response = self.createPUT(url, {'fulltime': True})
        bad_response = self.createPUT(bad_url, {'fulltime': True})
        game = models.Game.objects.get(id=2)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(bad_response.status_code, 400)
        self.assertEqual(game.fulltime, True)


    def test_game_teams(self):
        url = reverse("Teams", args=[2])
        bad_url = reverse("Teams", args=[1])
        self.client.login(username="user2", password="password1")

        # check only admin is allowed to set teams
        response = self.createPUT(url, {
            'player': 2,
            'team': "A"
        })
        bad_response = self.createPUT(bad_url, {
            'player': 2,
            'team': "A"
        })
        player = models.Player.objects.get(game=2, user=2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bad_response.status_code, 400)
        self.assertEqual(player.team, 'A')
