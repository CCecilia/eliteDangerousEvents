import lorem
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta
from .models import Event


class EventModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # dec vars
        today = timezone.now()
        tomorrow = timezone.now() + timedelta(days=1)
        start_date = today.date()
        start_time = today.time()
        end_date = tomorrow.date()
        end_time = start_time
        current_attendee_count = 0
        event_count = 0

        # create auth user
        User.objects.create(
            username='TestUser',
            email='test@user.com',
            password='password'
        )

        # create attendees for event
        while current_attendee_count < 5:
            username = 'TestUser%s' % current_attendee_count
            email = 'test%s@user.com' % current_attendee_count
            User.objects.create(
                username=username,
                email=email,
                password='password'
            )
            current_attendee_count += 1

        # Create Events
        while event_count < 5:
            event_name = 'Test Event %s' % event_count
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
                description=lorem.paragraph()
            )
            event_count += 1

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

    def test_index_view(self):
        response = self.client.get('')
        # check reponse and template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/index.html')

    def test_createEvent_view(self):
        response = self.client.get('/createEvent/')
        # check reponse and template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/createEvent.html')

    def test_allEvents_view(self):
        response = self.client.get('/myEvents/')
        # check redirect for user not signed in
        self.assertEqual(response.status_code, 302)

    def test_myEvents_view(self):
        response = self.client.get('/allEvents/')
        # check reponse and template
        self.assertEqual(response.status_code, 200)
        # cehck all events are returned
        self.assertTrue(len(response.context['events']) == 5)
        self.assertTemplateUsed(response, 'html/allEvents.html')

    def test_editEvent_view_(self):
        response = self.client.get('/event/edit/1/')
        # check reponse and template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/editEvent.html')
        # check correct event is returned
        correct_event = Event.objects.get(pk=1)
        self.assertEqual(response.context['event'], correct_event)
