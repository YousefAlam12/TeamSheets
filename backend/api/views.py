from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import User, Game
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
import json


def test_api_view(request):
    user_location = Point(0.105618, 51.549457, srid=4326)
    x = Game.objects.filter(location__distance_lt=(user_location, D(km=230)))
    print(x)

    return JsonResponse({
        'message': 'Good response!'
    })


def isAuthenticated(request):
    # checks to see if user is logged in to correctly restrict pages
    isAuth = request.user.is_authenticated
    print(isAuth)
    print(request.user)
    return JsonResponse({"isAuth": isAuth})


def login_api(request):
    # login view
    if request.user.is_authenticated:
        return

    if request.method == 'POST':
        POST = json.loads(request.body)
        username = POST['username']
        password = POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success': 'login successful'})

        else:
            return JsonResponse({'error': 'Invalid details'}, status=400)


@login_required
def logout_api(request):
    logout(request)
    return JsonResponse({'success': 'Logged Out'})


def signup(request):
    if request.user.is_authenticated:
        return

    if request.method == 'POST':
        POST = json.loads(request.body)
        print(POST)

        firstname = POST['firstname']
        lastname = POST['lastname']
        email = POST['email']
        dob = POST['dob']
        username = POST['username']
        password1 = POST['password1']
        password2 = POST['password2']

        # Check if passwords match
        if password1 != password2:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        try:
            # Create a new user
            newUser = User(
                first_name=firstname,
                last_name=lastname,
                email=email,
                date_of_birth=dob,
                username=username
            )
            newUser.set_password(password1)

            # Validate the user
            newUser.full_clean()
            newUser.save()
            login(request, newUser)

            return JsonResponse({'success': 'Account creation successful'})

        # Handle validation errors
        except ValidationError as e:
            errorMsg = next(iter(e.message_dict.values()))[0]
            return JsonResponse({'error': errorMsg}, status=400)
