from django.contrib import admin
from .models import Event, SolarSystem, LFGPost

admin.site.register(Event)
admin.site.register(LFGPost)
admin.site.register(SolarSystem)
