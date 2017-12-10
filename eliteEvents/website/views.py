__author__ = 'christian.cecilia1@gmail.com'

import os
import hashlib
from django.shortcuts import render
from django.http import JsonResponse
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
    password = str(request.POST['register-password']).encode('utf-8')
    h = hashlib.md5()

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
        # hash password
        h.update(password)

        # create user
        User.objects.create(
            username=username,
            email=email,
            password=h.hexdigest()
        )

        # create response
        response = {
            'status': 'success',
        }

    # send reponse JSON
    return JsonResponse(response)


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
