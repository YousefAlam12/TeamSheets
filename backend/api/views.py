from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .models import User
import json


def test_api_view(request):
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
            return JsonResponse({'success' : 'login successful'})

        else:
            return JsonResponse({'error': 'Invalid details'}, status=400)
