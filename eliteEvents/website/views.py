__author__ = 'christian.cecilia1@gmail.com'

import os
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import Event

# Global
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Pages


def index(request):
    context = {
        'page': 'index',
        'coverHeading': 'Search Events'
    }
    return render(request, 'html/index.html', context)


def signin(request):
    context = {
        'page': 'signin'
    }
    return render(request, 'html/signin.html', context)


def createEventPage(request):
    context = {
        'page': 'createEvent',
        'coverHeading': 'Create Event'
    }
    return render(request, 'html/createEvent.html', context)


def allEvents(request):
    # Get Events
    events = Event.objects.all()

    context = {
        'page': 'allEvents',
        'coverHeading': 'All Events',
        'events': events
    }
    return render(request, 'html/allEvents.html', context)


def myEvents(request):
    # Dec  Vars
    user = request.user
    events = Event.objects.filter(creator=user)
    
    context = {
        'page': 'myEvents',
        'coverHeading': 'My Events',
        'events': events
    }
    return render(request, 'html/myEvents.html', context)


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
    event_search = json.loads(request.body)['event_search']

    # filter for matching events and serialize for json
    event_search_results = list(Event.objects.filter(
        name__icontains=event_search
    ).values(
        'id',
        'name',
        'event_type',
        'start_date',
        'attendees'
    ))

    # create response
    response = {
        'status': 'success',
        'event_search_results': event_search_results
    }

    # send reponse JSON
    return JsonResponse(response)


def eventDetails(request):
    # get event
    event_id = json.loads(request.body)['event_id']
    event = Event.objects.get(id=event_id)

    # serialize json
    serialized_event = serializers.serialize('json', [event])
    print(serialized_event)
    # create response
    response = {
        'status': 'success',
        'event': serialized_event
    }

    # send reponse JSON
    return JsonResponse(response)


def eventJoin(request):
    # get event
    user_id = int(request.POST['user-id'])
    event_id = int(request.POST['event-id'])
    user = User.objects.get(id=user_id)
    event = Event.objects.get(id=event_id)

    # add user to event
    event.attendees.add(user)

    attendance = event.attendees.all().count()

    # create response
    response = {
        'status': 'success',
        'attendance': attendance
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
    event_title = str(request.POST['event-title']).title()
    event_type = str(request.POST['event-type'])
    event_location = str(request.POST['event-location'])
    event_description = str(request.POST['event-description'])
    event_start_date = str(request.POST['event-start-date'])
    event_start_time = str(request.POST['event-start-time'])
    event_end_date = str(request.POST['event-end-date'])
    event_end_time = str(request.POST['event-end-time'])
    user_id = int(request.POST['user-id'])
    creator = User.objects.get(id=user_id)

    # create event
    Event.objects.create(
        name=event_title,
        event_type=event_type,
        creator=creator,
        location=event_location,
        description=event_description,
        start_date=event_start_date,
        start_time=event_start_time,
        end_date=event_end_date,
        end_time=event_end_time
    )

    # #create response
    response = {
        'status': 'success',
    }

    # send reponse JSON
    return JsonResponse(response)
