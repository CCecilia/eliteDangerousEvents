from django.urls import path

from . import views

urlpatterns = [
    path('', views.HtmlRendering.index, name='index'),
    path('signin/', views.HtmlRendering.signin, name='signin'),
    path('createEvent/', views.HtmlRendering.createEventPage, name='createEventPage'),
    path('allEvents/', views.HtmlRendering.allEvents, name='allEvents'),
    path('myEvents/', views.HtmlRendering.myEvents, name='myEvents'),
    path('event/edit/<int:event_id>/', views.HtmlRendering.editEvent, name='editEvent'),
    path('register/', views.UserViews.register, name='register'),
    path('login/', views.UserViews.loginUser, name='loginUser'),
    path('logout/', views.UserViews.logoutUser, name='logoutUser'),
    path('event/update/<int:event_id>/', views.EventViews.updateEvent, name='updateEvent'),
    path('event/remove/', views.EventViews.removeEvent, name='removeEvent'),
    path('event/create/', views.EventViews.createEvent, name='createEvent'),
    path('event/search/', views.EventViews.searchEvents, name='searchEvents'),
    path('event/details/', views.EventViews.eventDetails, name='eventDetails'),
    path('event/join/', views.EventViews.eventJoin, name='eventJoin'),
    path('search/systems/', views.Utility.searchSystems, name='searchSystems')
]
