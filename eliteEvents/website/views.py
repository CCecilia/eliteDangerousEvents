__author__ = 'christian.cecilia1@gmail.com'

import ijson
import json
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, SolarSystem


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

@login_required
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

@login_required
def myEvents(request):
    # Dec  Vars
    user = request.user

    # redirect to signin page if user not found
    try:
        events = Event.objects.filter(creator=user)
    except TypeError:
        return redirect('signin')

    context = {
        'page': 'myEvents',
        'coverHeading': 'My Events',
        'events': events
    }
    return render(request, 'html/myEvents.html', context)

@login_required
def editEvent(request, event_id):
    # Dec  Vars
    event = get_object_or_404(Event, pk=event_id)
    context = {
        'page': 'editEvent',
        'coverHeading': 'Edit Event',
        'event': event
    }
    return render(request, 'html/editEvent.html', context)


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
    elif len(password) < 8:
        response = {
            'status': 'fail',
            'error_msg': 'password must be atleast 8 characters long'
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

    if user:
        login(request, user)
        # create response
        response = {
            'status': 'success'
        }
    else:
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
    event = get_object_or_404(Event, pk=event_id)

    # serialize json
    serialized_event = serializers.serialize('json', [event])

    # create response
    response = {
        'status': 'success',
        'event': serialized_event
    }

    # send reponse JSON
    return JsonResponse(response)

@login_required
def eventJoin(request):
    # get event
    user_id = int(request.POST['user-id'])
    event_id = int(request.POST['event-id'])
    user = request.user
    event = Event.objects.get(pk=event_id)

    # add user to event
    event.attendees.add(user)

    # get updated attendance count
    attendance = event.attendees.all().count()

    # create response
    response = {
        'status': 'success',
        'attendance': attendance
    }

    # send reponse JSON
    return JsonResponse(response)

@login_required
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
    creator = request.user

    # create event
    new_event = Event.objects.create(
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
        'event_id': new_event.id

    }

    # send reponse JSON
    return JsonResponse(response)

@login_required
def updateEvent(request, event_id):
    # dec vars
    event_title = str(request.POST['event-title']).title()
    event_type = str(request.POST['event-type'])
    event_location = str(request.POST['event-location'])
    event_description = str(request.POST['event-description'])
    event_start_date = str(request.POST['edit-event-start-date'])
    event_start_time = str(request.POST['edit-event-start-time'])
    event_end_date = str(request.POST['edit-event-end-date'])
    event_end_time = str(request.POST['edit-event-end-time'])
    event = get_object_or_404(Event, pk=event_id)

    # Update Event
    event.name = event_title
    event.event_type = event_type
    event.location = event_location
    event.description = event_description

    # only update new dates/times
    if event_start_date:
        event.start_date = event_start_date

    if event_end_date:
        event.end_date = event_end_date

    if event_start_time:
        event.start_time = event_start_time

    if event_end_time:
        event.end_time = event_end_time

    # Save updated event
    event.save()

    # create response
    response = {
        'status': 'success',
    }

    # send reponse JSON
    return JsonResponse(response)


def removeEvent(request):
    # dec vars
    event_id = json.loads(request.body)['event_id']
    event = get_object_or_404(Event, pk=event_id)

    # delete event
    event.delete()

    # create response
    response = {
        'status': 'success',
    }

    # send reponse JSON
    return JsonResponse(response)


def searchSystems(request):
    system_query = json.loads(request.body)['system_query']
    results = list(SolarSystem.objects.filter(name__icontains=system_query).values('name')[:5])

    # create response
    response = {
        'status': 'success',
        'results': results
    }

    # send reponse JSON
    return JsonResponse(response)


def parsePopulatedSystems(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    with open(BASE_DIR + '/website/media/uploads/populated_systems.json', "rb") as f:
        # parse JSON file
        parser = ijson.parse(f)
        for prefix, event, value in parser:
            if prefix == 'item.name':
                SolarSystem.objects.create(name=str(value))
                print('added value:{} to DB'.format(value))

    return