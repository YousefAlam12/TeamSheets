from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import datetime
from django.utils.timezone import now

from .models import User, Game, Player
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
import json


def test_api_view(request):
    # user_location = Point(0.105618, 51.549457)
    # user = User.objects.get(id=1)
    # user_location = user.location
    # x = Game.objects.filter(location__distance_lte=(user_location, D(km=5)))
    # games = [game.as_dict() for game in x]
    # print(x)
    # print(games[0]['players'])

    # return JsonResponse({
    #     'games': games
    # })

    user = User.objects.get(id=1)
    user_location = user.location
    x = Game.objects.annotate(distance=Distance('location', request.user.location)).order_by('distance', 'date')
    games = [game.as_dict() for game in x]

    return JsonResponse({
        'games': games
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
        postcode = POST['postcode']
        location = Point(POST['longitude'], POST['latitude'])
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
                postcode=postcode,
                location=location,
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


@login_required
# returns all games in db
def all_games_api(request):
    if request.method == 'GET':
        print('getting finished games...')
        games = Game.objects.all()
        data = [game.as_dict() for game in games]
        return JsonResponse({'games': data})


@login_required
# returns games which current user is in
def my_games_api(request):
    if request.method == 'GET':
        today = datetime.datetime.today().date()

        games = Game.objects.filter(fulltime=False, players=request.user, date__gte=today).order_by('date')
        myGames = [game.as_dict() for game in games]

        games = Game.objects.filter(admin=request.user).order_by('-date')
        admin_games = [game.as_dict() for game in games]

        games = Game.objects.filter(players=request.user, date__lt=today).order_by('-date')
        played_games = [game.as_dict() for game in games]

        return JsonResponse({'myGames': myGames,
                             'adminGames': admin_games,
                             'playedGames': played_games})


@login_required
# endpoint for games which create and return active games
def games_api(request):
    if request.method == 'POST':
        POST = json.loads(request.body)
        POST = POST['game']
        print(POST)

        # check if necessary fields are filled
        required_fields = ['name', 'date', 'start_time', 'end_time', 'totalPlayers', 'price', 'address', 'postcode', 'longitude', 'latitude']

        for field in required_fields:
            if not POST.get(field):
                return JsonResponse({'error': f'Missing field: {field}'}, status=400)

        # creating new game
        newGame = Game(
            name=POST['name'],
            date=POST['date'],
            start_time=datetime.datetime.strptime(POST['start_time'], '%H:%M'),
            end_time=datetime.datetime.strptime(POST['end_time'], '%H:%M'),
            description=POST['description'],
            totalPlayers=POST['totalPlayers'],
            price=POST['price'],
            address=POST['address'],
            postcode=POST['postcode'],
            location=Point(POST['longitude'], POST['latitude']),
            admin=request.user
        )
        newGame.save()

        # create new player for the game (admin)
        newPlayer = Player(
            user=request.user,
            game=newGame,
        )
        newPlayer.save()

    today = datetime.datetime.today().date()
    # games = Game.objects.filter(fulltime=False, date__gte=today).order_by('date')
    # orders games by distance from user
    games = Game.objects.annotate(distance=Distance('location', request.user.location)).filter(fulltime=False, date__gte=today).order_by('distance', 'date')
    data = [game.as_dict() for game in games]
    return JsonResponse({'games': data})


@login_required
# endpoint for a game, handles joining/leaving game and pay status
def game_api(request, game_id):
    game = Game.objects.get(id=game_id)
    player = Player.objects.filter(user=request.user, game=game)

    # checks if user is a player of the game
    if player.count() > 0:
        player = Player.objects.get(user=request.user, game=game)
        paid = player.paid
    else:
        paid = None

    if request.method == 'GET':
        return JsonResponse({'user': request.user.as_dict(),
                            'paid': paid,
                             'game': game.as_dict()})

    # user joins game
    if request.method == 'POST':
        POST = json.loads(request.body)
        print(POST)

        if POST.get('join'):
            print('joining game')
            player = Player(
                user=request.user,
                game=game,
            )
            player.save()

    # leaves the user from the game
    if request.method == 'DELETE':
        DELETE = json.loads(request.body)
        print(DELETE)

        if DELETE.get('leave'):
            print('-------------------------------')
            print('leaving game')
            player.delete()

    # sets the pay status
    if request.method == 'PUT':
        PUT = json.loads(request.body)

        if PUT.get('paid'):
            player.paid = True
            player.save()

    # sends the game and pay status as dict to update the page
    return JsonResponse({'game': game.as_dict(),
                        'paid': player.paid})


@login_required
# api for choosing teams in the game page
def teams_api(request, game_id):
    game = Game.objects.get(id=game_id)

    if request.method == 'PUT':
        PUT = json.loads(request.body)
        print(PUT)

        player = Player.objects.get(user=PUT['player'], game=game_id)

        # if player is on the same team as button clicked team will reset
        if player.team == PUT['team']:
            player.team = None
        else:
            player.team = PUT['team']

        player.save()

        return JsonResponse({'game': game.as_dict()})
