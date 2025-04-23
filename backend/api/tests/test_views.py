from django.test import TestCase, Client
from api import models
import json
from django.urls import reverse
from datetime import date, time, timedelta, datetime
from django.contrib.gis.geos import Point
from django.contrib.auth import authenticate

# NOTE: exceptions are thrown due to email notifications being locked but this can be ignored as tests still work
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
        self.user4 = models.User.objects.create_user(
            first_name="user4", last_name="testing", username="user4", password="password1", email="user4@email.com", date_of_birth=date(2000, 1, 1), postcode="E1 0QE", location=Point(-0.045764, 51.515359)
        )

        d = date(2027, 8, 22)
        start_t = time(12, 00)
        end_t = time(14, 00)

        # test games
        self.game1 = models.Game.objects.create(name="Game 1", date=d, start_time=start_t, end_date=d, end_time=end_t, totalPlayers=10, price=5, address="Mile End Park Leisure Centre, Rhodeswell Rd, London", postcode="E3 4HL", location=Point(-0.031997, 51.519437), admin=self.user1, is_private=False, fulltime=False)
        self.game2 = models.Game.objects.create(name="Game 2", date=d, start_time=start_t, end_date=d, end_time=end_t, totalPlayers=10, price=5, address="Fairlop Oaks Playing Fields, Forest Rd, Ilford", postcode="IG6 3HX", location=Point(0.100324, 51.598645), admin=self.user2, is_private=False, fulltime=False)
        self.privateGame = models.Game.objects.create(name="Private", date=d, start_time=start_t, end_date=d, end_time=end_t, totalPlayers=10, price=5, address="Mile End Park Leisure Centre, Rhodeswell Rd, London", postcode="E3 4HL", location=Point(-0.031997, 51.519437), admin=self.user3, is_private=True, fulltime=False)
        self.fulltimeGame = models.Game.objects.create(name="Fulltime", date=d, start_time=start_t, end_date=d, end_time=end_t, totalPlayers=10, price=5, address="Fairlop Oaks Playing Fields, Forest Rd, Ilford", postcode="IG6 3HX", location=Point(0.100324, 51.598645), admin=self.user2, is_private=False, fulltime=True)

        # GAME 1 test players
        models.Player.objects.create(user=self.user3, game=self.game1)

        # GAME 2 test players
        models.Player.objects.create(user=self.user1, game=self.game2)
        models.Player.objects.create(user=self.user2, game=self.game2)

        # FULLTIMEGAME test players
        models.Player.objects.create(user=self.user1, game=self.fulltimeGame)
        models.Player.objects.create(user=self.user2, game=self.fulltimeGame)
        models.Player.objects.create(user=self.user3, game=self.fulltimeGame)
        
        # PRIVATE GAME test players
        models.Player.objects.create(user=self.user1, game=self.privateGame)

        # Friend users
        self.user3.friends.add(self.user4)
        self.user4.friends.add(self.user3)

        # Rating objects
        models.Rating.objects.create(rater=self.user1, ratee=self.user2, game=self.fulltimeGame, attack=8, defence=4, strength=7, speed=7, technique=6)


    # Setup Method for team balancing algorithm test
    def team_balance_setup(self):
        d = date(2027, 8, 22)
        start_t = time(12, 00)
        end_t = time(14, 00)

        # create test users
        for i in range(10):
            models.User.objects.create_user(
                first_name=f"player{i+1}", last_name="testing", username=f"p{i+1}", password="password1", email=f"p{i+1}@email.com", date_of_birth=date(2000, 1, 1), postcode="IG11 9BX", location=Point(0.105618, 51.549457)
            )
        p1 = models.User.objects.get(username="p1")
        game = models.Game.objects.create(name="Team Balance Game", date=d, start_time=start_t, end_date=d, end_time=end_t, totalPlayers=10, price=5, address="Fairlop Oaks Playing Fields, Forest Rd, Ilford", postcode="IG6 3HX", location=Point(0.100324, 51.598645), admin=p1, is_private=False, fulltime=False)

        # create test players for test game
        for i in range(10):
            user = models.User.objects.get(username=f"p{i+1}")
            models.Player.objects.create(user=user, game=game)

        def getUser(username): return models.User.objects.get(username=username)
        
        # creating ratings for test players
        models.Rating.objects.create(rater=self.user1, ratee=getUser("p1"), game=self.fulltimeGame, attack=9, defence=5, strength=7, speed=7, technique=5)
        models.Rating.objects.create(rater=self.user1, ratee=getUser("p2"), game=self.fulltimeGame, attack=3, defence=9, strength=9, speed=6, technique=6)
        models.Rating.objects.create(rater=self.user1, ratee=getUser("p3"), game=self.fulltimeGame, attack=7, defence=6, strength=4, speed=5, technique=8)
        models.Rating.objects.create(rater=self.user1, ratee=getUser("p4"), game=self.fulltimeGame, attack=4, defence=6, strength=7, speed=6, technique=2)
        models.Rating.objects.create(rater=self.user1, ratee=getUser("p5"), game=self.fulltimeGame, attack=2, defence=4, strength=5, speed=8, technique=2)
        models.Rating.objects.create(rater=self.user1, ratee=getUser("p6"), game=self.fulltimeGame, attack=2, defence=2, strength=5, speed=5, technique=4)
        models.Rating.objects.create(rater=self.user1, ratee=getUser("p7"), game=self.fulltimeGame, attack=4, defence=8, strength=5, speed=5, technique=9)
        models.Rating.objects.create(rater=self.user1, ratee=getUser("p8"), game=self.fulltimeGame, attack=5, defence=5, strength=4, speed=7, technique=6)
        models.Rating.objects.create(rater=self.user1, ratee=getUser("p9"), game=self.fulltimeGame, attack=7, defence=8, strength=6, speed=5, technique=7)
        models.Rating.objects.create(rater=self.user1, ratee=getUser("p10"), game=self.fulltimeGame, attack=5, defence=5, strength=5, speed=5, technique=5)


        game = models.Game.objects.get(name="Team Balance Game")
        return game


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
        self.assertEqual(len(res.get('userList')), 3)


    def test_friends_POST(self):
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


    def test_friends_DELETE(self):
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

        # login as user3 to check if user is able to remove friend
        self.client.logout()
        self.client.login(username="user3", password="password1")
        get_response = self.client.get(url).json()
        response  = self.createDELETE(url, {'unfriending': get_response['user']['friends'][0].get('id')})
        res = response.json()

        # checks users are removed from friends list in database ann response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res['user']['friends']), 0)
        self.assertEqual(len(self.user3.friends.all()), 0)
        self.assertEqual(len(self.user4.friends.all()), 0)
    

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

        # checks it displays games based on location 
        self.assertEqual(res['games'][0].get('name'), "Game 2")


    def test_games_POST(self):
        url = reverse("Games")
        self.client.login(username="user1", password="password1")
    
        response = self.createPOST(url, {
            'game' : {
                'name': "Test Game",
                'date': "2027-08-12",
                'start_time': "12:00",
                'end_date': "2027-08-12",
                'end_time': "14:00",
                'description': "testing 123.......",
                'totalPlayers': 10,
                'price': 5,
                'address': "Fairlop Oaks Playing Fields, Forest Rd, Ilford",
                'postcode': "IG6 3HX",
                'longitude': 0.100324,
                'latitude': 51.598645,
                'privacy': False
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

        # only admin and players/invited should be able to view private game
        url = reverse("Game_api", args=[3])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        self.client.login(username="user3", password="password1")
        url = reverse("Game_api", args=[3])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # user who is not player or admin of game should not be able to view private game
        self.client.logout()
        self.client.login(username="user2", password="password1")
        url = reverse("Game_api", args=[3])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)


    # Checks joining games
    def test_game_POST(self):
        url = reverse("Game_api", args=[1])
        self.client.login(username="user2", password="password1")

        # checks user joining new game
        response = self.createPOST(url, {'join' : True})
        player = models.Player.objects.filter(game=1, user=2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(player), 1)

        # checks user joining game they're already in
        url = reverse("Game_api", args=[2])
        response = self.createPOST(url, {'join' : True})
        player = models.Player.objects.filter(game=2, user=2)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(player), 1)

        # checks user joining private game without invite
        url = reverse("Game_api", args=[3])
        response = self.createPOST(url, {'join' : True})
        self.assertEqual(response.status_code, 400)
        
        # checks user joining fulltime game
        self.client.logout()
        self.client.login(username="user4", password="password1")
        url = reverse("Game_api", args=[4])
        response = self.createPOST(url, {'join' : True})
        self.assertEqual(response.status_code, 400)


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

    
    # Checks game subcription toggle
    def test_game_SUBSCRIBE(self):
        url = reverse("Game_api", args=[2])
        game = models.Game.objects.get(id=2)
        self.client.login(username="user1", password="password1")

        # checks subscribing
        response = self.createPUT(url, {'subscribe' : True})
        notification = models.Notification.objects.filter(game=game)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(notification), 1)

        # checks unsubscribing
        response = self.createDELETE(url, {'unsubscribe' : True})
        notification = models.Notification.objects.filter(game=game)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(notification), 0)


    # Checks user updating pay status
    def test_game_PAY(self):
        url = reverse("Game_api", args=[2])
        self.client.login(username="user2", password="password1")

        response = self.createPUT(url, {'paid': True})
        player = models.Player.objects.get(game=2, user=2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(player.paid, True)


    # tests all admin PUT methods in game_api
    def test_game_PUT(self):
        # url is game where user is admin and bad_url is where it is not
        url = reverse("Game_api", args=[2])
        bad_url = reverse("Game_api", args=[1])
        self.client.login(username="user2", password="password1")

        # checks game privacy changes (only admin)
        response = self.createPUT(url, {'toggle_privacy': True})
        bad_response = self.createPUT(bad_url, {'toggle_privacy': True})
        game = models.Game.objects.get(id=2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bad_response.status_code, 400)
        self.assertEqual(game.is_private, True)

        # checks if description is changed (only admin)
        response = self.createPUT(url, {'description': "changing description"})
        bad_response = self.createPUT(bad_url, {'description': "changing description"})
        game = models.Game.objects.get(id=2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bad_response.status_code, 400)
        self.assertEqual(game.description, "changing description")

        # checks game is set to fulltime (only admin)
        response = self.createPUT(url, {'fulltime': True})
        bad_response = self.createPUT(bad_url, {'fulltime': True})
        game = models.Game.objects.get(id=2)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(bad_response.status_code, 400)
        self.assertEqual(game.fulltime, True)


    def test_teams(self):
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

        response = self.createPUT(url, {
            'player': 2,
            'team': "B"
        })
        player = models.Player.objects.get(game=2, user=2)
        
        self.assertEqual(player.team, 'B')


    def test_ratings(self):
        url = reverse("Ratings", args=[4])
        self.client.login(username="user1", password="password1")
        response = self.client.get(url)
        res = response.json()

        # checks that rated players are returned (user is included)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res['ratedPlayers']), 2)

        # checks that post creates new rating object
        response = self.createPOST(url, {
            'ratings': {
                'attack': 4,
                'defence': 7,
                'strength': 7,
                'speed': 5,
                'technique': 5,
            },
            'player': 3
        })
        res = response.json()
        rating = models.Rating.objects.filter(rater=self.user1, ratee=self.user3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res['ratedPlayers']), 3)
        self.assertEqual(len(rating), 1)

        # Checks user is unable to rate a player already rated
        response = self.createPOST(url, {
            'ratings': {
                'attack': 4,
                'defence': 7,
                'strength': 7,
                'speed': 5,
                'technique': 5,
            },
            'player': 3
        })
        rating = models.Rating.objects.filter(rater=self.user1, ratee=self.user3)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(res['ratedPlayers']), 3)
        self.assertEqual(len(rating), 1)

        # Checks user cannot rate game not at fulltime
        bad_url = reverse("Ratings", args=[2])
        response = self.client.get(bad_url)
        self.assertEqual(response.status_code, 400)

        # Checks user who didnt play cannot rate
        self.client.logout()
        self.client.login(username="user4", password="password1")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)


    def test_gameInvite(self):
        private_url = reverse("Game Invite", args=[3])
        public_url = reverse("Game Invite", args=[1])
        self.client.login(username="user3", password="password1")

        # Sending invite method check (POST)
        private_response = self.createPOST(private_url, {'to_user' : 2})
        public_response = self.createPOST(public_url, {'to_user' : 2})
        invite = models.GameInvite.objects.filter(from_user=self.user3, to_user=2)
        self.assertEqual(private_response.status_code, 200)
        self.assertEqual(public_response.status_code, 200)
        self.assertEqual(len(invite), 2)        

        # Change user to handle invite
        self.client.logout()
        self.client.login(username="user2", password="password1")

        # Checks that invited player is able to view private game
        publicGame_url = reverse("Game_api", args=[1])
        privateGame_url = reverse("Game_api", args=[3])
        response = self.client.get(privateGame_url)
        self.assertEqual(response.status_code, 200)

        # Checks cancelling game invitation (DELETE)
        response = self.createDELETE(private_url, {'game_invite' : 1})
        response = self.createDELETE(public_url, {'game_invite' : 2})
        invite = models.GameInvite.objects.filter(from_user=self.user3, to_user=2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(invite), 0)

        # When invite is canceled/cleared user should be able to view public game but not private
        response = self.client.get(privateGame_url)
        self.assertEqual(response.status_code, 400)
        response = self.client.get(publicGame_url)
        self.assertEqual(response.status_code, 200)


    def test_matchmake(self):
        url = reverse("Matchmake")
        self.client.login(username="user2", password="password1")
        response = self.client.get(url)
        res = response.json()

        # checks if games are filtered based on user's stats
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res['games']), 1)
        self.assertEqual(res['games'][0].get('name'), "Game 2")


    def test_balanceTeams(self):
        game = self.team_balance_setup()
        url = reverse("Balance Teams", args=[game.id])

        # checks that only admin can access api
        self.client.login(username="p2", password="password1")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)

        # switch to admin 
        self.client.logout()
        self.client.login(username="p1", password="password1")
        
        ad_balance = []
        skill_balance = []

        # running team balance 5 times to find the average in the balance scores against different teams (to flatten outliers)
        for i in range(5):
            response = self.client.get(url)
            res = response.json()

            self.assertEqual(response.status_code, 200)

            # check to see stats of teams are balanced in accordance to the 2 objectives (attack/defence and skills)
            A_attack = 0
            A_defence = 0
            A_skill = 0
            
            B_attack = 0
            B_defence = 0
            B_skill = 0

            players = res['game']['players']
            for p in players:
                if p['team'] == "A":
                    A_attack += p['stats']['attack']
                    A_defence += p['stats']['defence']
                    A_skill += (p['stats']['strength'] + p['stats']['speed'] + p['stats']['technique']) / 3

                if p['team'] == "B":
                    B_attack += p['stats']['attack']
                    B_defence += p['stats']['defence']
                    B_skill += (p['stats']['strength'] + p['stats']['speed'] + p['stats']['technique']) / 3

            ad_diff = abs((A_attack + A_defence) - (B_attack + B_defence))
            skill_diff = abs(A_skill - B_skill)

            ad_balance.append(ad_diff)
            skill_balance.append(skill_diff)

        ad_test = sum(ad_balance) / len(ad_balance)
        skill_test = sum(skill_balance) / len(skill_balance)

        # checks the average balance score is within threshold/reason
        self.assertLessEqual(ad_test, 5)
        self.assertLessEqual(skill_test, 5)