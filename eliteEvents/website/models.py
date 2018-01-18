from django.db import models
from datetime import datetime
import pytz
from django.contrib.auth.models import User

XBOX = 'XB'
PLAYSTATION = 'PS'
PC = 'PC'

PLATFORMS = {
    (XBOX, 'XBox'),
    (PLAYSTATION, 'Playstation'),
    (PC, 'Computer')
}


class Event(models.Model):

    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=200, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    attendees = models.ManyToManyField(User, related_name='attendees')
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    location = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default='Please add a description')
    platform = models.CharField(max_length=2, choices=PLATFORMS, default=PC)
    discord_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class LFGPost(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    platform = models.CharField(max_length=2, choices=PLATFORMS, default=PC)
    post_type = models.CharField(max_length=200, null=True)
    discord_link = models.URLField(blank=True, null=True, default='Not Given')
    commander = models.CharField(max_length=200, null=False, blank=False)
    location = models.CharField(max_length=200, null=True, default='Not Given')
    ship = models.CharField(max_length=200, default='sidewinder')
    rank = models.CharField(max_length=200, default='harmless')
    message = models.TextField(max_length=300, blank=False, null=False)

    def __str__(self):
        return self.id

    def timeSinceCreation(self):
        utc_now_aware = datetime.utcnow().replace(tzinfo=pytz.utc)
        time_since_timedelta = utc_now_aware - self.date_created
        time_since_secs = time_since_timedelta.seconds
        time_since_mins = (time_since_secs // 60) % 60
        time_since_hrs = time_since_secs // 3600

        if time_since_hrs >= 1:
            time_since = 'over an hour ago'
        elif time_since_mins < 60 and time_since_mins >= 1:
            time_since = 'about {} mins ago'.format(time_since_mins)
        elif time_since_secs < 60:
            time_since = 'less than {} secs ago'.format(time_since_secs)

        return time_since


class SolarSystem(models.Model):
    name = models.CharField(db_index=True, max_length=200)

    def __str__(self):
        return self.name
