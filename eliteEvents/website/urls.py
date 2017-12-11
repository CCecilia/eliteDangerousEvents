from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('createEvent/', views.createEventPage, name='createEventPage'),
    path('event/create/', views.createEvent, name='createEvent'),
    path('event/search/', views.searchEvents, name='searchEvents'),
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='loginUser'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('searchSolarSystems/', views.searchSolarSystems, name='searchSolarSystems'),
]
