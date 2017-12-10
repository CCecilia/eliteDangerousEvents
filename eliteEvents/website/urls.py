from django.urls import path

from . import views

urlpatterns = [
	# Pages
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    # Ajax
    path('searchEvents/', views.searchEvents, name='searchEvents'),
    path('register/', views.register, name='register'),
]