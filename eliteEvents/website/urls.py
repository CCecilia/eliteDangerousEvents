from django.urls import path

from . import views

app_name = 'website'

urlpatterns = [
    path('', views.HtmlRendering.index, name='index'),
    path('signin/', views.HtmlRendering.signin, name='signin'),
    path('createEvent/', views.HtmlRendering.createEventPage, name='createEventPage'),
    path('allEvents/', views.HtmlRendering.allEvents, name='allEvents'),
    path('myEvents/', views.HtmlRendering.myEvents, name='myEvents'),
    path('event/edit/<int:event_id>/', views.HtmlRendering.editEvent, name='editEvent'),
    path('lfg/', views.HtmlRendering.lfgPage, name='lfgPage'),
    path('register/', views.UserViews.register, name='register'),
    path('login/', views.UserViews.loginUser, name='loginUser'),
    path('logout/', views.UserViews.logoutUser, name='logoutUser'),
    path('setUserTz/', views.UserViews.setUserTz, name='setUserTz'),
    path('event/update/<int:event_id>/', views.EventViews.updateEvent, name='updateEvent'),
    path('event/remove/', views.EventViews.removeEvent, name='removeEvent'),
    path('event/create/', views.EventViews.createEvent, name='createEvent'),
    path('event/search/', views.EventViews.searchEvents, name='searchEvents'),
    path('event/details/', views.EventViews.eventDetails, name='eventDetails'),
    path('event/join/', views.EventViews.eventJoin, name='eventJoin'),
    path('lfg/create/', views.LFGViews.createLfgPost, name='createLfgPost'),
    path('lfg/check/', views.LFGViews.checkForNew, name='checkForNew'),
    path('search/systems/', views.Utility.searchSystems, name='searchSystems'),
    path('sitemap.xml', views.Utility.sitemap, name='sitemap'),
    path('robots.txt', views.Utility.robots, name='robots')
]
