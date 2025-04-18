from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import datetime
from .models import User, Game, Player, Rating, FriendRequest, GameInvite, Notification
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
import threading
import json

# pymoo
import numpy as np
import random
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.operators.mutation.pm import PM



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
        ad_balance = []
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
            ad_diff = abs((team_stats[0]['attack'] + team_stats[0]['defence']) - (team_stats[1]['attack'] + team_stats[1]['defence']))
            skill_diff = abs(team_stats[0]['skill'] - team_stats[1]['skill'])

            ad_balance.append(ad_diff)
            skill_balance.append(skill_diff)

        # Assign objectives to minimize
        out["F"] = np.column_stack([ad_balance, skill_balance])


@login_required
def balanceTeams(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except:
        return JsonResponse({'error': 'game does not exist'}, status=400)

    if not isAdmin(request.user, game):
        return JsonResponse({'error': 'only admin is allowed to do this'}, status=400)
    
    players = Player.objects.filter(game=game_id).select_related('user')

    player_settings = {
        12: (25, 60),
        14: (40, 70),
        16: (50, 70),
        18: (50, 80),
        20: (50, 90),
        22: (50, 100)
    }

    # Default values
    population_size = 20
    n_gen = 50

    # adjust pop_size and generations to get more balanced results
    if game.totalPlayers in player_settings:
        population_size, n_gen = player_settings[game.totalPlayers]

    # creating and solving the balancing problem using nsga-ii
    problem = TeamBalancingProblem(players)
    algorithm = NSGA2(pop_size=population_size, mutation=PM(prob=0.3))

    result = minimize(problem, algorithm, termination=("n_gen", n_gen), verbose=False)

    # getting all soluitions where they have equal/fair amount of players
    valid_solutions = []

    for x in result.X:
        playerTeams = list(map(round, x))
        if playerTeams.count(playerTeams[0]) == len(playerTeams) // 2:
            valid_solutions.append(playerTeams)

    # removing duplicate solutions to allow for different teams
    best_solutions = []
    [best_solutions.append(s)
    for s in valid_solutions if s not in best_solutions]
    if len(best_solutions) <= 0:
        return JsonResponse({'error': 'error in balancing'}, status=400)

    best_solution = random.choice(best_solutions)

    teamA = []
    teamB = []

    # Assigning teams to player objects based on solution to update page
    for i, team in enumerate(best_solution):
        if team <= 0:
            teamA.append(players[i].user.username)
            players[i].team = 'A'
        else:
            teamB.append(players[i].user.username)
            players[i].team = 'B'

        players[i].save()

    return JsonResponse({'game': game.as_dict()})


def isAuthenticated(request):
    # checks to see if user is logged in to correctly restrict pages
    if request.user.is_authenticated:
        return JsonResponse({"isAuth": True,
                             'user': request.user.as_dict()})
    else:
        return JsonResponse({"isAuth": False})


def login_api(request):
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
def send_friend_request(request):
    if request.method == 'POST':
        POST = json.loads(request.body)
        from_user = request.user
        to_user = User.objects.get(id=POST['to_user'])
        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=from_user, to_user=to_user)
        if created:
            # send an notification to the user being invited (thread to prevent frontend loading)
            threading.Thread(
                target=requestNotification, 
                args=(
                    f"Friend request from {request.user}",
                    f"You have received a friend from {request.user}. \n\n Check it out on TeamSheets.",
                    to_user.email)
                    ).start()
            return JsonResponse({'user': request.user.as_dict()})
        else:
            return JsonResponse({'error': 'friend request already exists'}, status=400)


@login_required
def friends_api(request):
    userList = User.objects.all()
    userList = [{'id': user.id, 'username': user.username} for user in userList]
    userList = list(filter(lambda u: u.get('id') != request.user.id, userList))

    if request.method != 'GET':
        JSON = json.loads(request.body)
        friend_request = FriendRequest.objects.get(from_user=JSON['from_user'], to_user=request.user)
        from_user = User.objects.get(id=friend_request.from_user.id)

        if request.method == 'POST':
            if friend_request.to_user == request.user:
                friend_request.to_user.friends.add(friend_request.from_user)
                friend_request.from_user.friends.add(friend_request.to_user)
                friend_request.delete()

                # send an notification to the user being invited (thread to prevent frontend loading)
                threading.Thread(
                    target=requestNotification, 
                    args=(
                        f"Now friends with {request.user.username}",
                        f"You are now friends with {request.user.username}. \n\n Check it out on TeamSheets.",
                        from_user.email)
                        ).start()
            else:
                return JsonResponse({'error': 'user does not exist'}, status=400)

        if request.method == 'DELETE':
            if friend_request.to_user == request.user:
                friend_request.delete()
            else:
                return JsonResponse({'error': 'user does not exist'}, status=400)

    return JsonResponse({'userList': userList,
                        'user': request.user.as_dict()
                        })


@login_required
# returns games user is linked with
def my_games_api(request):
    if request.method == 'GET':
        today = datetime.datetime.now()

        games = Game.objects.filter(
            Q(date__gt=today) | Q(date=today.date()) & Q(end_time__gte=today.time()), fulltime=False, players=request.user).order_by('date')
        myGames = [game.as_dict() for game in games]

        games = Game.objects.filter(admin=request.user).order_by('-date')
        admin_games = [game.as_dict() for game in games]

        games = Game.objects.filter(
            fulltime=True, players=request.user).order_by('-date')
        played_games = [game.as_dict() for game in games]

        return JsonResponse({'myGames': myGames,
                             'adminGames': admin_games,
                             'playedGames': played_games,
                             'user': request.user.as_dict()})


@login_required
# endpoint for games which create and return active games
def games_api(request):
    if request.method == 'POST':
        POST = json.loads(request.body)
        POST = POST['game']

        # check if necessary fields are filled
        required_fields = ['name', 'date', 'start_time', 'end_time',
                           'totalPlayers', 'price', 'address', 'postcode', 'longitude', 'latitude']

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
            is_private=POST['is_private'],
            admin=request.user
        )
        newGame.save()

        # create new player for the game (admin)
        newPlayer = Player(
            user=request.user,
            game=newGame,
        )
        newPlayer.save()

    # orders games by distance from user
    today = datetime.datetime.now()
    games = Game.objects.annotate(distance=Distance('location', request.user.location)).filter(
        Q(date__gt=today) | Q(date=today.date()) & Q(end_time__gte=today.time()), fulltime=False, is_private=False).order_by('distance', 'date')
    data = [game.as_dict() for game in games]
    if len(data) <= 0:
        data = None
    return JsonResponse({'games': data})


# helper function for game admin checks
def isAdmin(user, game):
    if user == game.admin:
        return True
    else:
        return False


@login_required
# endpoint for a game, handles all game operations
def game_api(request, game_id):
    # checks if game exists
    try:
        game = Game.objects.get(id=game_id)
    except:
        return JsonResponse({'error': 'game does not exist'}, status=400)

    player = Player.objects.filter(user=request.user, game=game)
    
    # only allows admin and players/invited to view private game
    if game.is_private and request.user != game.admin:
        gameInvite = request.user.invite_to.filter(game=game)
        if player.count() <= 0 and gameInvite.count() <= 0:
            return JsonResponse({'error': 'user not allowed to view game'}, status=400)


    # checks if user is a player of the game
    if player.count() > 0:
        player = Player.objects.get(user=request.user, game=game)
        paid = player.paid
    else:
        paid = None
        player = None

    if request.method == 'GET':
        return JsonResponse({
                            'paid': paid,
                             'game': game.as_dict(),
                             })

    # user joins game
    if request.method == 'POST':
        POST = json.loads(request.body)

        if POST.get('join'):
            # validates if game is joinable
            currentPlayers = Player.objects.filter(game=game_id)
            if len(currentPlayers) >= game.totalPlayers or game.fulltime:
                return JsonResponse({'error': "game is not joinable"}, status=400)

            # validates if user is already a player
            player, created = Player.objects.get_or_create(user=request.user, game=game)
            if not created:
                return JsonResponse({'error': "player already exists"}, status=400)

            # send email to subscribers (thread to prevent frontend loading)
            threading.Thread(
                target=gameNotification, 
                args=(
                    game,
                    f"{player.user.username} joined {game.name}",
                    f"{player.user.username} has now joined {game.name} scheduled for: {game.date} from {game.start_time}-{game.end_time}.")
                    ).start()

            # remove all game invitations to the game when joining
            game_invites = GameInvite.objects.filter(to_user=request.user, game=game)
            if len(game_invites) > 0:
                for inv in game_invites:
                    inv.delete()

    # DELETE methods for game
    if request.method == 'DELETE':
        DELETE = json.loads(request.body)

        # player leaves game
        if DELETE.get('leave'):
            if player == None:
                return JsonResponse({'error': "player does not exists"}, status=400)

            # send email to subscribers (thread to prevent frontend loading)
            threading.Thread(
                target=gameNotification, 
                args=(
                    game,
                    f"{player.user.username} left {game.name}",
                    f"{player.user.username} has now left {game.name} scheduled for: {game.date} from {game.start_time}-{game.end_time}.")
                    ).start()
            player.delete()
            removeNotifications(user=request.user, game=game)
        
        # admin removes player
        if DELETE.get('kick'):
            # request only allowed if user is admin
            if not isAdmin(request.user, game):
                return JsonResponse({'error': 'only admin is allowed to do this'}, status=400)
            
            player = Player.objects.get(user=DELETE['kick'], game=game)
            # send email to all players/subscribers
            gameNotification(
                game,
                f"{player.user.username} kicked from {game.name}",
                f"{player.user.username} has now been kicked from {game.name} scheduled for: {game.date} from {game.start_time}-{game.end_time}.",
                kickEmail=player.user.email
            )
            player.delete()
            removeNotifications(user=DELETE['kick'], game=game)

        # admin cancels game removing game from system
        if DELETE.get('cancel_game'):
            # request only allowed if user is admin
            if not isAdmin(request.user, game):
                return JsonResponse({'error': 'only admin is allowed to do this'}, status=400)

            # send email to all players/subscribers
            gameNotification(
                game,
                f"{game.name} is cancelled",
                f"{game.name} scheduled for: {game.date} from {game.start_time}-{game.end_time} has now been cancelled.",
                True
            )
            game.delete()
            return JsonResponse({'success' : 'game is deleted'})

        # user disables notifications
        if DELETE.get('unsubscribe'):
            notificaton = Notification.objects.get(game=game, user=request.user)
            notificaton.delete()
            return JsonResponse({'user': request.user.as_dict()})

    # PUT methods for game
    if request.method == 'PUT':
        PUT = json.loads(request.body)

        # sets the pay status
        if PUT.get('paid'):
            if player == None:
                return JsonResponse({'error': "player does not exists"}, status=400)
            
            player.paid = True
            player.save()

        # admin calls fulltime on game
        if PUT.get('fulltime'):
            # request only allowed if user is admin
            if not isAdmin(request.user, game):
                return JsonResponse({'error': 'only admin is allowed to do this'}, status=400)
            
            game.fulltime = True
            game.save()

            # send email to all players/subscribers
            threading.Thread(
                target=gameNotification, 
                args=(
                    game,
                    f"Fulltime for {game.name}",
                    f"It's fulltime, it's time to rate all the players!!",
                    True)
                    ).start()

        # changes privacy of game
        if PUT.get('toggle_privacy'):
            # request only allowed if user is admin
            if not isAdmin(request.user, game):
                return JsonResponse({'error': 'only admin is allowed to do this'}, status=400)
            
            game.is_private = not game.is_private
            game.save()

        # user allows notifications
        if PUT.get('subscribe'):
            # prevents invited users from subbing to private games when they are not a player
            gameInvite = request.user.invite_to.filter(game=game)
            if gameInvite.count() > 0 and game.is_private:
                return JsonResponse({'error': 'only players can subscribe to a private game'}, status=400)
            
            notification = Notification(game=game, user=request.user)
            notification.save()
            return JsonResponse({'user': request.user.as_dict()})
        
        # admin can change description of game
        if PUT.get('description'):
            # request only allowed if user is admin
            if not isAdmin(request.user, game):
                return JsonResponse({'error': 'only admin is allowed to do this'}, status=400)
            
            game.description = PUT.get('description')
            game.save()

    # sends the game and pay status as dict to update the page
    return JsonResponse({'game': game.as_dict(),
                        'paid': player.paid,
                        'user' : request.user.as_dict()})


@login_required
# api for manually choosing teams in game page
def teams_api(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except:
        return JsonResponse({'error': 'game does not exist'}, status=400)

    # only allows entry if user is the admin of the game
    if not isAdmin(request.user, game):
        return JsonResponse({'error': 'only admin is allowed to do this'}, status=400)

    if request.method == 'PUT':
        PUT = json.loads(request.body)
        player = Player.objects.get(user=PUT['player'], game=game_id)

        # if player is on the same team as button clicked team will reset
        if player.team == PUT['team']:
            player.team = None
        else:
            player.team = PUT['team']

        player.save()

        return JsonResponse({'game': game.as_dict()})


@login_required
# api for users to rate each other and update stats
def ratings_api(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except:
        return JsonResponse({'error': 'game does not exist'}, status=400)
    
    isPlaying = Player.objects.filter(user=request.user, game=game)

    # allow entry if user actually played in game and fulltime is called
    if isPlaying.count() <= 0 or (not game.fulltime):
        return JsonResponse({'error': 'Cannot rate this game'}, status=400)

    # finds players user already rated to prevent double rating
    ratedPlayers = Rating.objects.filter(rater=request.user, game=game_id)

    if request.method == 'POST':
        POST = json.loads(request.body)
        playerRated = User.objects.get(id=POST['player'])
        POST = POST['ratings']

        # Validation checks
        try:
            attack = float(POST['attack'])
            defence = float(POST['defence'])
            strength = float(POST['strength'])
            speed = float(POST['speed'])
            technique = float(POST['technique'])
        except:
            return JsonResponse({'error': 'Must rate all attributes.'}, status=400)

        if (ratedPlayers.filter(ratee=playerRated)):
            return JsonResponse({'error': 'Already rated this player'}, status=400)

        # Create rating if checks pass
        rating = Rating(
            rater=request.user,
            ratee=playerRated,
            game=game,
            attack=attack,
            defence=defence,
            strength=strength,
            speed=speed,
            technique=technique
        )
        rating.save()

    rated_players = [rating.ratee.as_dict() for rating in ratedPlayers]
    rated_players.append(request.user.as_dict())

    return JsonResponse({'game': game.as_dict(),
                        'ratedPlayers': rated_players})


@login_required
# api handling invitations to games
def gameInvite(request, game_id):
    game = Game.objects.get(id=game_id)
    player = Player.objects.filter(user=request.user, game=game)

    if request.method == 'POST':
        # only admin and players are allowed to invite in private games
        if game.is_private and (not isAdmin(request.user, game)) and player.count() <= 0:
            return JsonResponse({'user': 'Only players can invite in private games'}, status=400)
        
        POST = json.loads(request.body)
        to_user = User.objects.get(id=POST['to_user'])

        game_invite, created = GameInvite.objects.get_or_create(
            from_user=request.user, to_user=to_user, game=game)
        
        # Does not create if user is already a player in game
        player_check = Player.objects.filter(user=to_user, game=game)
        if len(player_check) > 0:
            return JsonResponse({'error': 'User is already a player in the game'}, status=400) 

        # send an notification to the user being invited (thread to prevent frontend loading)
        threading.Thread(
                target=requestNotification, 
                args=(
                    f"Game Invite for {game.name}",
                    f"You have been invited by {request.user.username} to {game.name} scheduled for: {game.date} from {game.start_time}-{game.end_time}. \n\n Go check it out on TeamSheets.",
                    to_user.email)
                    ).start()
        
        return JsonResponse({'success': 'user has been invited'})

    # rejects game invite
    if request.method == 'DELETE':
        DELETE = json.loads(request.body)
        game_invite = GameInvite.objects.get(id=DELETE['game_invite'])
        game_invite.delete()

        return JsonResponse({'user': request.user.as_dict()})


# helper funcition sends email notification about game statuses
def gameNotification(game, subject, message, include_players=False, kickEmail=None):
    subscribers = Notification.objects.filter(game=game.id)
    recipients = [sub.user.email for sub in subscribers]

    if kickEmail != None:
        recipients.append(kickEmail)
    
    if include_players:
        players = Player.objects.filter(game=game)
        p = [player.user.email for player in players]

        for email in p:
            if email not in recipients:
                recipients.append(email)

    send_mail(
        subject,
        message,
        'settings.EMAIL_HOST_USER',
        recipients,
        fail_silently=False,
    )
    

# helper function sends email notification about invites/friendrequests statuses
def requestNotification(subject, message, recipient):
    send_mail(
        subject,
        message,
        'settings.EMAIL_HOST_USER',
        [recipient],
        fail_silently=False,
    )


# helper function removes notification objs
def removeNotifications(user, game):
    notification = Notification.objects.filter(game=game, user=user)
    if len(notification) > 0:
        for notif in notification:
            notif.delete()



@login_required
# api for profile page
def profile_api(request):
    user = request.user
    
    # changes user details
    if request.method == 'PUT':
        PUT = json.loads(request.body)

        user.email = PUT['email']
        user.postcode = PUT['postcode']
        user.location = Point(PUT['longitude'], PUT['latitude'])

        try:
            user.full_clean()
            user.save()
        except ValidationError as e:
            errorMsg = next(iter(e.message_dict.values()))[0]
            return JsonResponse({'error': errorMsg}, status=400)

    return JsonResponse({'user': request.user.as_dict(),
                        'email': request.user.email,
                        'postcode': request.user.postcode})


@login_required
# api for changing password
def password_api(request):
    user = request.user

    # changes password after validation
    if request.method == 'PUT':
        PUT = json.loads(request.body)
        valid = authenticate(username=user.username, password=PUT['old'])
        if valid is None or PUT['new'] == '':
            return JsonResponse({'error': 'error'}, status=400)
        else:
            user.set_password(PUT['new'])
            user.save()
            login(request, user)

    return JsonResponse({'user': user.as_dict()})


def matchmake_api(request):
    userRating = request.user.overallRating
    recommended_games = []
    today = datetime.datetime.now()
    games = Game.objects.annotate(distance=Distance('location', request.user.location)).filter(
        Q(date__gt=today) | Q(date=today.date()) & Q(end_time__gte=today.time()), fulltime=False, is_private=False).order_by('distance', 'date')
    
    # finds recommended games based on user's stats
    for game in games:
        gameRating = 0
        players = Player.objects.filter(game=game)
        
        # calculates game's overall rating based on players stats
        for p in players:
            gameRating += p.user.overallRating

        gameRating /= len(players)
        gameRating = round(gameRating, 1)
        
        if (userRating-1.5) <= gameRating <= (userRating+1.5):
            recommended_games.append(game)

    data = [game.as_dict() for game in recommended_games]
    return JsonResponse({'games': data})