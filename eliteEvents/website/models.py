from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField('date created')

    def __str__(self):
        return self.name
