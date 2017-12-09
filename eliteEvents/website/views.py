__author__ = 'christian.cecilia1@gmail.com'

import os
from django.shortcuts import render
from django.http import JsonResponse
from .models import *

# Global
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Pages


def index(request):
    context = {
    	'page': 'index'
    }
    return render(request, 'html/index.html', context)


def signin(request):
    context = {
    	'page':'signin'
    }
    return render(request, 'html/signin.html', context)


# AJAX


def searchEvents(request):
    # dec vars
    query = str(request.POST['event-search'])
    print(query)

    # create response
    response = {
        'status': 200,
    }

    # send reponse JSON
    return JsonResponse(response)
