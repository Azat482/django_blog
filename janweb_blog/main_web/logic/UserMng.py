from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import IntegrityError

def AuthUser(req, data):
    user = authenticate(
        req, 
        username = data['username'], 
        password = data['password']
        )
    if user is not None:
        login(req, user)
        return True
    else:
        return False

def AddUser(data):
    try:
        User.objects.create_user(
            username=data['username'], 
            password=data['password'],
            email=data['email']
            )
    except Exception as e:
        return e
    else:
        return True
        

def LogoutUser(request):
    logout(request)

