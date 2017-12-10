__author__ = 'christian.cecilia1@gmail.com'

import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Event

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
        'page': 'signin'
    }
    return render(request, 'html/signin.html', context)


def createEventPage(request):
    context = {
        'page': 'createEvent'
    }
    return render(request, 'html/createEvent.html', context)


# AJAX


def register(request):
    # dec vars
    username = str(request.POST['register-username']).lower()
    email = str(request.POST['register-email']).lower()
    password = str(request.POST['register-password'])

    # check if username or email is used
    username_check = User.objects.filter(username=username)
    email_check = User.objects.filter(email=email)

    if username_check:
        response = {
            'status': 'fail',
            'error_msg': 'username already in use'
        }
    elif email_check:
        response = {
            'status': 'fail',
            'error_msg': 'email already in use'
        }
    else:
        # create user
        user = User.objects.create_user(username, email, password)

        # login user
        login(request, user)

        # create response
        response = {
            'status': 'success',
        }

    # send reponse JSON
    return JsonResponse(response)


def loginUser(request):
    # dec vars
    username = request.POST['signin-username']
    password = request.POST['signin-password']
    # Auth user 
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        # create response
        response = {
            'status': 'success'
        }
    else:
        print('login failed')
        # create response
        response = {
            'status': 'fail'
        }

    # send reponse JSON
    return JsonResponse(response)


def logoutUser(request):
    # log out user
    logout(request)

    # send to home page
    return redirect('index')


def searchEvents(request):
    # dec vars
    query = str(request.POST['event-search'])
    print(query)

    # create response
    response = {
        'status': 'success',
    }

    # send reponse JSON
    return JsonResponse(response)


@csrf_exempt
def searchSolarSystems(request):
    # dec vars
    solar_system = str(request.POST['query'])

    print(solar_system)

    # create response
    response = {
        'status': 'success',
    }

    # send reponse JSON
    return JsonResponse(response)


def createEvent(request):
    # dec vars
    event_title = str(request.POST['event-title'])
    event_type = str(request.POST['event-type'])
    event_location = str(request.POST['event-location'])
    event_description = str(request.POST['event-description'])
    event_start_date = str(request.POST['event-start-date'])
    event_start_time = str(request.POST['event-start-time'])
    event_end_date = str(request.POST['event-end-date'])
    event_end_time = str(request.POST['event-end-time'])
    user_id = int(request.POST['user-id'])
    creator = User.objects.get(id=user_id)

    print(event_start_date,'\n',event_start_time)

    # event_start_formatted = datetime.strptime(event_start_date + ' ' +event_start_time, '%Y %b %d  %I:%M%p')
    # event_end_formatted = datetime.strptime(event_end_date + ' ' +event_end_time, '%Y %b %d  %I:%M%p')

    event_start_formatted =event_start_date + ' ' +event_start_time
    event_end_formatted = event_end_date + ' ' +event_end_time

    print(event_start_formatted, '\n', event_end_formatted)
    # create event
    Event.objects.create(
            name=event_title,
            event_type=event_type,
            creator=creator,
            location=event_location,
            description=event_description,
            start_date=event_start_formatted,
            end_date=event_end_formatted
    	)

    # #create response
    response = {
        'status': 'success',
    }

    # send reponse JSON
    return JsonResponse(response)
