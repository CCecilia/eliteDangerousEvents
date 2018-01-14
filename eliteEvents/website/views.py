__author__ = 'christian.cecilia1@gmail.com'
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
import ijson
import json
import os
import pytz
from .models import Event, SolarSystem


class HtmlRendering:

    def index(request):
        all_events = Event.objects.all().order_by('-attendees')
        featuredEvents = all_events[:8]

        context = {
            'page': 'index',
            'coverHeading': 'Search Events',
            'featuredEvents': featuredEvents
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
        events = Event.objects.all().order_by('start_date')

        try:
            # filter out users own events if logged
            events = events.exclude(creator=request.user)
        except TypeError:
            pass

        page = request.GET.get('page')
        paginator = Paginator(events, 20)

        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            events = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            events = paginator.page(paginator.num_pages)

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
        created_page = request.GET.get('created_page')
        joined_page = request.GET.get('joined_page')

        # redirect to signin page if user not found
        try:
            created_events = Event.objects.filter(creator=user).order_by('start_date')
            joined_events = Event.objects.filter(attendees=user).order_by('start_date')
        except TypeError:
            return redirect('signin')
        
        created_paginator = Paginator(created_events, 20)
        joined_paginator = Paginator(joined_events, 20)

        try:
            created_events = created_paginator.page(created_page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            created_events = created_paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            created_events = created_paginator.page(created_paginator.num_pages)

        try:
            joined_events = joined_paginator.page(joined_page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            joined_events = joined_paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            joined_events = joined_paginator.page(joined_paginator.num_pages)

        context = {
            'page': 'myEvents',
            'coverHeading': 'My Events',
            'created_events': created_events,
            'joined_events': joined_events
        }
        return render(request, 'html/myEvents.html', context)

    @login_required
    def editEvent(request, event_id):
        # Dec  Vars
        event = get_object_or_404(Event, pk=event_id)
        local_tz = request.session['django_timezone']

        event.start_date = Utility.toLocal(event.start_date.date(), event.start_date.time(), pytz.timezone(local_tz))
        event.end_date = Utility.toLocal(event.end_date.date(), event.end_date.time(), pytz.timezone(local_tz))

        context = {
            'page': 'editEvent',
            'coverHeading': 'Edit Event',
            'event': event
        }
        return render(request, 'html/editEvent.html', context)


class UserViews:

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
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

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
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
        return redirect(HtmlRendering.index)

    def setUserTz(request):
        request.session['django_timezone'] = request.POST['timezone']
        return JsonResponse({'status': 200})


class EventViews:

    @login_required
    def createEvent(request):
        # dec vars
        event_title = str(request.POST['event-title']).title()
        event_type = str(request.POST['event-type'])
        event_platform = str(request.POST['platform-type'])
        event_location = str(request.POST['event-location'])
        event_description = str(request.POST['event-description'])
        event_start_date = str(request.POST['event-start-date'])
        event_start_time = str(request.POST['event-start-time'])
        event_end_date = str(request.POST['event-end-date'])
        event_end_time = str(request.POST['event-end-time'])
        discord_link = str(request.POST['discord-link'])
        time_zone = request.session['django_timezone']
        local_tz = pytz.timezone(time_zone)
        creator = request.user
        start_date = Utility.toUTC(event_start_date, event_start_time, local_tz)
        end_date = Utility.toUTC(event_end_date, event_end_time, local_tz)

        # check start/end dt's make sense
        if start_date < datetime.now(pytz.utc):
            # create response
            response = {
                'status': 'fail',
                'error_msg': 'Start date needs to be in the future.'
            }
        elif start_date > end_date:
            # create response
            response = {
                'status': 'fail',
                'error_msg': 'End date/time has to come after start date/time.'
            }
        else:
            # create event
            new_event = Event.objects.create(
                name=event_title,
                event_type=event_type,
                creator=creator,
                location=event_location,
                description=event_description,
                start_date=start_date,
                end_date=end_date,
                platform=event_platform,
                discord_link=discord_link
            )

            # create response
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
        time_zone = request.session['django_timezone']
        discord_link = str(request.POST['discord-link'])
        local_tz = pytz.timezone(time_zone)
        event = get_object_or_404(Event, pk=event_id)

        
        
        # Update Event
        event.name = event_title
        event.event_type = event_type
        event.location = event_location
        event.description = event_description
        event.discord_link = discord_link

        # handle start/end dt's
        try:
            start_date = Utility.toUTC(event_start_date, event_start_time, local_tz)
            end_date = Utility.toUTC(event_end_date, event_end_time, local_tz)
            
            if start_date < datetime.now(pytz.utc):
                # create response
                response = {
                    'status': 'fail',
                    'error_msg': 'Start date needs to be in the future.'
                }
            elif start_date > end_date:
                # create response
                response = {
                    'status': 'fail',
                    'error_msg': 'End date/time has to come after start date/time.'
                }

            event.start_date = start_date
            event.end_date = end_date
        # if date was unaltered it came in as humanized string; pass
        except ValueError:
            pass

        # Save updated event
        event.save()

        # create response
        response = {
            'status': 'success',
        }

        # send reponse JSON
        return JsonResponse(response)

    @login_required
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
    
    @login_required
    def eventJoin(request):
        # get event
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
            'attendees',
            'platform'
        ))

        # reformat start dates
        for i in event_search_results[:10]:
            i['start_date'] = i['start_date'].date()

        # create response
        response = {
            'status': 'success',
            'event_search_results': event_search_results[:10]
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


class Utility:

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

    def toUTC(date, time, local_tz):
        # convert to localized dt obj
        aware_local_dt = local_tz.localize(
            datetime.strptime(
                '{} {}'.format(date, time),
                '%Y-%m-%d %H:%M'
            )
        )

        # convert to utc dt obj
        utc_dt = aware_local_dt.astimezone(pytz.utc)

        return utc_dt

    def toLocal(date, time, local_tz):
        # convert utc dt obj
        aware_utc_dt = pytz.utc.localize(
            datetime.strptime(
                '{} {}'.format(date, time),
                '%Y-%m-%d %H:%M:%S'
            )
        )

        # convert to local dt
        local_dt = aware_utc_dt.astimezone(local_tz)

        return local_dt

    def cleanEndedEvents():
        # # get end events
        # ended_events = Event.objects.filter(end_date__lte=timezone.now())

        # for event in ended_events:
        #     event.delete()

        for event in Event.objects.all():
            event.name = 'task ran'
            event.save()

        return



class TimezoneMiddleware(MiddlewareMixin):


    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
    