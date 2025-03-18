from django.test import TestCase, Client
from api import models
import json
from django.urls import reverse
from datetime import date
from django.contrib.gis.geos import Point


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = models.User.objects.create_user(
            first_name="user1", last_name="testing", username="user1", password="password1", email="user1@email.com", date_of_birth=date(2000, 1, 1), postcode="IG11 9BX", location=Point(0.105618, 51.549457)
        )
        self.user2 = models.User.objects.create_user(
            first_name="user2", last_name="testing", username="user2", password="password1", email="user2@email.com", date_of_birth=date(2000, 1, 1), postcode="IG11 9BX", location=Point(0.105618, 51.549457)
        )


    def createPOST(self, url, data):
        response = self.client.post(url, data, content_type='application/json')
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
            'firstname': "user1",
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
        self.assertEqual(len(res.get('userList')), 1)


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

        # checks if sending user is added to friends
        self.assertEqual(len(res['user']['friends']), 1)
        self.assertEqual(len(self.user2.friends.all()), 1)

        # FriendRequest object should be deleted
        friend_requests = models.FriendRequest.objects.all()
        self.assertEqual(len(friend_requests), 0)