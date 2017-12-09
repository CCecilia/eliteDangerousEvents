from django.db import models
import uuid


class User(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Event(models.Model):
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField('date created')

    def __str__(self):
        return self.name
