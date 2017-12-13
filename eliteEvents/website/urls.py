from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('createEvent/', views.createEventPage, name='createEventPage'),
    path('event/create/', views.createEvent, name='createEvent'),
    path('event/search/', views.searchEvents, name='searchEvents'),
    path('event/details/', views.eventDetails, name='eventDetails'),
    path('event/join/', views.eventJoin, name='eventJoin'),
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='loginUser'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('allEvents/', views.allEvents, name='allEvents'),
    path('myEvents/', views.myEvents, name='myEvents'),
    path('event/edit/<int:event_id>/', views.editEvent, name='editEvent'),
    path('event/update/<int:event_id>/', views.updateEvent, name='updateEvent'),
    path('event/remove/', views.removeEvent, name='removeEvent'),
]
