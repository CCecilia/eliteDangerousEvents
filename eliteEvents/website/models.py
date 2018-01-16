from django.db import models
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
    discord_link = models.URLField(blank=True, null=True)
    commander = models.CharField(max_length=200, null=False, blank=False)
    location = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.id


class SolarSystem(models.Model):
    name = models.CharField(db_index=True, max_length=200)

    def __str__(self):
        return self.name
