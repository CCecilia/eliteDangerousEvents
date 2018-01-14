
from datetime import timedelta
from django.test import TestCase, Client, tag
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import json
import lorem

from .models import Event, SolarSystem


class EventModelTests(TestCase):
    c = Client()

    @classmethod
    def setUpTestData(self):

        # dec vars
        today = timezone.now()
        tomorrow = timezone.now() + timedelta(days=1)
        start_date = today.date()
        start_time = today.time()
        end_date = tomorrow.date()
        end_time = start_time

        # create auth user
        User.objects.create(
            username='TestUser',
            email='test@user.com',
            password='password'
        )

        # create attendees for event
        for i in range(5):
            username = 'TestUser%s' % i
            email = 'test%s@user.com' % i
            User.objects.create(
                username=username,
                email=email,
                password='password'
            )

        # Create Events
        for i in range(50):
            event_name = 'Test Event %s' % i
            Event.objects.create(
                name=event_name,
                event_type='Combat',
                creator=User.objects.get(pk=1),
                start_date=start_date,
                start_time=start_time,
                end_date=end_date,
                end_time=end_time,
                location='Sol',
                date_created=timezone.now(),
                description=lorem.paragraph(),
                discord_link='https://discord.gg/MN8m55'
            )

        # joined user 2 to all events
        for event in Event.objects.all():
            user = User.objects.get(pk=2)
            event.attendees.add(user)

    def test_event_associated_to_auth_user(self):
        # check if event will return creator
        event = Event.objects.get(pk=1)
        user = event.creator
        self.assertEqual(user.id, 1)

    def test_attendees_added_to_event(self):
        # exclude creator from attendees
        test_attendees = User.objects.all().exclude(pk=1)
        event = Event.objects.get(pk=1)

        # add attendees to event
        for attendee in test_attendees:
            event.attendees.add(attendee)

        self.assertEqual(event.attendees.all().count(), 5)

    @tag('quick')
    def test_allEvents_view(self):
        response = self.c.get(reverse('website:allEvents'))
        # check reponse and template
        self.assertEqual(response.status_code, 200)
        # cehck all events are returned
        self.assertTrue(len(response.context['events']) == 20)
        self.assertTemplateUsed(response, 'html/allEvents.html')

        # test second page
        response = self.c.get('/allEvents/?page=2')
        # check reponse and template
        self.assertEqual(response.status_code, 200)
        # cehck all events are returned
        self.assertTrue(len(response.context['events']) == 20)
        self.assertTemplateUsed(response, 'html/allEvents.html')

        # test third page
        response = self.c.get('/allEvents/?page=3')
        # check reponse and template
        self.assertEqual(response.status_code, 200)
        # cehck all events are returned
        self.assertTrue(len(response.context['events']) == 10)
        self.assertTemplateUsed(response, 'html/allEvents.html')

    def test_editEvent_view_redirect(self):
        response = self.c.get(reverse('website:editEvent', kwargs={'event_id':1}))
        
        # check reponse and template
        self.assertEqual(response.status_code, 302)

    def test_editEvent_view(self):
        user = User.objects.get(pk=1)
        self.c.force_login(user)
        response = self.c.get(reverse('website:editEvent', kwargs={'event_id':1}))
        
        # check reponse and template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/editEvent.html')

        # check correct event is returned
        correct_event = Event.objects.get(pk=1)
        self.assertEqual(response.context['event'], correct_event)

    @tag('quick')
    def test_search_events(self):
        # Check event search
        response = self.c.post(
            reverse('website:searchEvents'), 
            json.dumps({'event_search': 'Test Event'}),
            'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        event_search_results = json.loads(response.content)['event_search_results']
        # Check event objs are returned
        self.assertEqual(len(event_search_results), 10)
        # check event objs have values
        for i in range(len(event_search_results)):
            self.assertFalse(event_search_results[i]['id'] == '')
            self.assertFalse(event_search_results[i]['name'] == '')
            self.assertFalse(event_search_results[i]['event_type'] == '')
            self.assertEqual(event_search_results[i]['attendees'], 2)

    @tag('quick')
    def test_event_details(self):
        # Check event deatils
        response = self.c.post(
            reverse('website:eventDetails'),
            json.dumps({'event_id': 1}),
            'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        event = json.loads(response.content)['event']

        # Check event obj is returned
        self.assertTrue(event)

    def test_join_event(self):
        event = Event.objects.get(pk=1)
        user = User.objects.get(pk=1)
        old_attendance = event.attendees.all().count()
        
        # login user
        self.c.force_login(user)

        # Check event search
        response = self.c.post(reverse('website:eventJoin'), {
            'event-id': 1
        })
        new_attendance = json.loads(response.content)['attendance']

        # Check attendance is updated
        self.assertEqual(new_attendance, old_attendance + 1)

    def test_create_event(self):
        today = timezone.now()
        init_event_count = Event.objects.all().count()
        user = User.objects.get(pk=1)
        
        # login user
        self.c.force_login(user)

        # Check event create
        response = self.c.post(reverse('website:createEvent'), {
            'event-title': 'test create event',
            'event-type': 'combat',
            'event-location': 'ltt 9455',
            'event-description': lorem.paragraph,
            'event-start-date': today.date(),
            'event-end-date': today.date(),
            'event-end-time': today.time(),
            'event-start-time': today.time(),
            'platform-type': 'PC',
            'discord-link': 'https://discord.gg/MN8m55'
        })

        new_event_count = Event.objects.all().count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_event_count, init_event_count + 1)

    def test_update_event(self):
        today = timezone.now()
        user = User.objects.get(pk=1)

        # login user
        self.c.force_login(user)

        # Check event create
        response = self.c.post('/event/edit/2/', {
            'event-title': 'edited',
            'event-type': 'exploration',
            'event-location': 'edited',
            'event-description': 'edited',
            'event-start-date': today.date(),
            'event-end-date': today.date(),
            'event-end-time': today.time(),
            'event-start-time': today.time()
        })
       
        self.assertEqual(response.status_code, 200)

    @tag('quick')
    def test_myEvents_redirect(self):
        response = self.c.get(reverse('website:myEvents'))
        # check reponse and template
        self.assertEqual(response.status_code, 302)

    @tag('quick')
    def test_myEvents_redirect(self):
        user_1 = User.objects.get(pk=1)
        user_2 = User.objects.get(pk=2)

        self.c.force_login(user_1)

        response = self.c.get(reverse('website:myEvents'))
        # check reponse and template
        self.assertEqual(response.status_code, 200)
        # # check all events are returned
        self.assertTrue(len(response.context['created_events']) == 20)
        self.assertTrue(len(response.context['joined_events']) == 0)
        self.assertTemplateUsed(response, 'html/myEvents.html')

        # test second page
        response = self.c.get('/myEvents/?created_page=2')
        # check reponse and template
        self.assertEqual(response.status_code, 200)
        # cehck all events are returned
        self.assertTrue(len(response.context['created_events']) == 20)
        self.assertEqual(len(response.context['joined_events']), 0)
        self.assertTemplateUsed(response, 'html/myEvents.html')

        # test joined events
        self.c.force_login(user_2)

        response = self.c.get(reverse('website:myEvents'))
        # # check all events are returned
        self.assertTrue(len(response.context['created_events']) == 0)
        self.assertTrue(len(response.context['joined_events']) == 20)
        self.assertTemplateUsed(response, 'html/myEvents.html')
        self.c.force_login(user_2)

        response = self.c.get('/myEvents/?joined_page=3')
        # # check all events are returned
        self.assertTrue(len(response.context['created_events']) == 0)
        self.assertTrue(len(response.context['joined_events']) == 10)
        self.assertTemplateUsed(response, 'html/myEvents.html')


class RenderViewsTests(TestCase):
    c = Client()

    @classmethod
    def setUpTestData(self):
        # create auth user
        User.objects.create(
            username='TestUser',
            email='test@user.com',
            password='password'
        )

    @tag('quick')
    def test_index_view(self):
        response = self.c.get(reverse('website:index'))
        # check reponse and template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/index.html')

    @tag('quick')
    def test_createEventPage_view(self):
        user = User.objects.get(pk=1)
        self.c.force_login(user)

        response = self.c.get(reverse('website:createEventPage'))
        
        # check reponse and template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/createEvent.html')

    def test_createEventPage_view_redirect(self):
        response = self.c.get(reverse('website:createEventPage'))
        # check reponse and template
        self.assertEqual(response.status_code, 302)

    def test_allEvents_view(self):
        response = self.c.get(reverse('website:myEvents'))
        # check redirect for user not signed in
        self.assertEqual(response.status_code, 302)

    def test_signin_view(self):
        response = self.c.get(reverse('website:signin'))
        # check redirect for user not signed in
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/signin.html')


class AjaxViewsTests(TestCase):
    c = Client()

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username='testuser',
            email='testuser@email.com',
            password='password'
        )

        for i in range(5):
            SolarSystem.objects.create(name="LTT 944{}".format(i) )

    @tag('quick')
    def test_ajax_register_success(self):
        # Check register success
        response = self.c.post(reverse('website:register'), {
            'register-username': 'testuser1',
            'register-email': 'testuser1@email.com',
            'register-password': 'password',
        })
        self.assertEqual(json.loads(response.content)['status'], 'success')
        self.assertEqual(response.status_code, 200)

    def test_ajax_register_username_in_use(self):
        # Check register failed  username taken
        response = self.c.post(reverse('website:register'), {
            'register-username': 'testuser',
            'register-email': 'testuser@email.com',
            'register-password': 'password'
        })
        self.assertEqual(json.loads(response.content)['status'], 'fail')
        self.assertEqual(json.loads(response.content)['error_msg'], 'username already in use')
      
    def test_ajax_register_email_in_use(self):
        # Check register failed email in use
        response = self.c.post(reverse('website:register'), {
            'register-username': 'testuser1',
            'register-email': 'testuser@email.com',
            'register-password': 'password'
        })
        self.assertEqual(json.loads(response.content)['status'], 'fail')
        self.assertEqual(json.loads(response.content)['error_msg'], 'email already in use')

    def test_ajax_register_password_length(self):
        # Check register failed  password length
        response = self.c.post(reverse('website:register'), {
            'register-username': 'testuser2',
            'register-email': 'testuser2@email.com',
            'register-password': 'pass'
        })
        self.assertEqual(json.loads(response.content)['status'], 'fail')
        self.assertEqual(json.loads(response.content)['error_msg'], 'password must be atleast 8 characters long')

    def test_ajax_login_fail(self):
        # Check login fail
        response = self.c.post(reverse('website:loginUser'), {
            'signin-username': 'testuser5000',
            'signin-password': 'password'
        })
        self.assertEqual(json.loads(response.content)['status'], 'fail')

    @tag('quick')
    def test_ajax_login_success(self):
        # Check login success
        response = self.c.post(reverse('website:loginUser'), {
            'signin-username': 'testuser',
            'signin-password': 'password'
        })
        self.assertEqual(response.status_code, 200)

    def test_search_systems(self):
        # Check systems search
        response = self.c.post(
            reverse('website:searchSystems'), 
            json.dumps({'system_query': 'LTT'}),
            'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        results = json.loads(response.content)['results']
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(results), 5)
