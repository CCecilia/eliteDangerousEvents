__author__ = 'christian.cecilia1@gmail.com'

import os
import hashlib
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *

# Global
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Pages


def index(request):
    context = {
        'page': 'index'
    }
    return render(request, 'html/index.html', context)


def signin(request):
    context = {
        'page': 'signin'
    }
    return render(request, 'html/signin.html', context)


# AJAX


def register(request):
    # dec vars
    username = str(request.POST['register-username']).lower()
    email = str(request.POST['register-email']).lower()
    password = str(request.POST['register-password'])

    # check if username or email is used
    username_check = User.objects.filter(username=username)
    email_check = User.objects.filter(email=email)

    if username_check:
        response = {
            'status': 'fail',
            'error_msg': 'username already in use'
        }
    elif email_check:
        response = {
            'status': 'fail',
            'error_msg': 'email already in use'
        }
    else:
        # create user
        user = User.objects.create_user(username, email, password)

        # login user
        login(request, user)

        # create response
        response = {
            'status': 'success',
        }

    # send reponse JSON
    return JsonResponse(response)


def loginUser(request):
    # dec vars
    username = request.POST['signin-username']
    password = request.POST['signin-password']
    print(request.POST['csrfmiddlewaretoken'])
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        # create response
        response = {
            'status': 'success'
        }
    else:
        print('login failed')
        # create response
        response = {
            'status': 'fail'
        }

    # send reponse JSON
    return JsonResponse(response)


def logoutUser(request):
    # log out user
    logout(request)

    # send to home page
    return redirect('index')


def searchEvents(request):
    # dec vars
    query = str(request.POST['event-search'])
    print(query)

    # create response
    response = {
        'status': 200,
    }

    # send reponse JSON
    return JsonResponse(response)
