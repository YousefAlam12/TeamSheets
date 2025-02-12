from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import datetime
from django.utils.timezone import now

##########################################################
# remember to update requirements.txt
import numpy as np
import random
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.operators.mutation.pm import PM
##########################################################

from .models import User, Game, Player
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
import json

###############################################################################################
# Helper class for team balancing 

# NSGA-II problem for team balancing
class TeamBalancingProblem(Problem):
    def __init__(self, players):
        self.players = players

        # Each player goes into one of the teams 0 or 1 in accordance to 2 objectives determining balance
        super().__init__(n_var=len(players),
                         n_obj=2,
                         n_constr=0,
                         xl=0,
                         xu=1,
                         type_var=int)

    def _evaluate(self, x, out, *args, **kwargs):
        attack_balance = []
        defence_balance = []
        skill_balance = []

        for solution in x:
            team_stats = {team: {"attack": 0, "defence": 0, 'skill': 0}
                          for team in range(2)}
                          
            # Assign players to teams
            for i, x in enumerate(solution):
                player = self.players[i]
                team = round(x)
                
                if player.user.stats != None:
                    team_stats[team]["attack"] += player.user.stats["attack"]
                    team_stats[team]["defence"] += player.user.stats["defence"]
                    team_stats[team]["skill"] += (player.user.stats["strength"] + player.user.stats["speed"] + player.user.stats["technique"])/3
                else:
                    # if player is new stats will just be set to 5 by default
                    team_stats[team]["attack"] += 5
                    team_stats[team]["defence"] += 5
                    team_stats[team]["skill"] += 5

            # Calculate balances (minimize differences between teams)
            attack_diff = abs((team_stats[0]['attack'] + team_stats[0]['skill']) - (team_stats[1]['attack'] + team_stats[1]['skill']))
            defence_diff = abs((team_stats[0]['defence'] + team_stats[0]['skill']) - (team_stats[1]['defence'] + team_stats[1]['skill']))

            attack_balance.append(attack_diff)
            defence_balance.append(defence_diff)


        # Assign objectives to minimize
        out["F"] = np.column_stack([attack_balance, defence_balance])
###############################################################################################


@login_required
def balanceTeams(request, game_id):
    players = Player.objects.filter(game=game_id).select_related('user')

    # try find sweet spot for different size game and change params 

    # creating and solving the balancing problem using nsga-ii
    problem = TeamBalancingProblem(players)
    # algorithm = NSGA2(pop_size=50, mutation=PM(prob=0.3))
    algorithm = NSGA2(pop_size=20, mutation=PM(prob=0.3))

    # result = minimize(problem, algorithm, termination=("n_gen", 100), verbose=False)
    result = minimize(problem, algorithm, termination=("n_gen", 50), verbose=False)

    # getting all soluitions where they have equal/fair amount of players
    valid_solutions = []

    for x in result.X:
        playerTeams = list(map(round, x))
        if playerTeams.count(playerTeams[0]) == len(playerTeams) // 2:
            valid_solutions.append(playerTeams)

    # removing duplicate solutions to allow different teams to be given on second call
    best_solutions = []
    [best_solutions.append(s) for s in valid_solutions if s not in best_solutions]
    best_solution = random.choice(best_solutions)

    teamA = []
    teamB = []

    for i, team in enumerate(best_solution):
        if team <= 0:
            teamA.append(players[i].user.username)
            players[i].team = 'A'
        else:
            teamB.append(players[i].user.username)
            players[i].team = 'B'

        players[i].save()

    print('===Team A===')
    print(teamA)

    print('\n===Team B===')
    print(teamB)

    game = Game.objects.get(id=game_id)
    return JsonResponse({'game': game.as_dict()})


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

    # user = User.objects.get(id=1)
    # user_location = user.location
    # x = Game.objects.annotate(distance=Distance('location', request.user.location)).order_by('distance', 'date')
    # games = [game.as_dict() for game in x]

    # return JsonResponse({
    #     'games': games
    # })

    print(request.user.stats)
    return JsonResponse({
        'user': request.user.as_dict(),
        # 'stats': request.user.stats
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

# @login_required
# def balanceTeams(request, game_id):
#     players = Player.objects.filter(game=game_id).select_related('user')

#     for i in range(len(players)):
#         print(players[i].user.username)
#         print(players[i].user.stats)
#         print(players[i].team, '\n')
#         # break

#     return JsonResponse({'balance team end point' : 'hi !!!!!!!'})