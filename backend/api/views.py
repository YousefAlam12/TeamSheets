from django.shortcuts import render
from django.http import JsonResponse


def test_api_view(request):
    return JsonResponse({
        'message': 'Good response!'
    })
