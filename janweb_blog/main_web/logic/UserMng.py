from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import IntegrityError
from ..models import UserProfile
import datetime


class SiteUserManager:
    def __init__(self):
        pass
    
    def AuthUser(self, req, data):
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

    def AddUser(self, data):
        try:
            user = User.objects.create_user(
                username=data['username'], 
                password=data['password'], 
                email=data['email']
                )
            account = UserProfile()
            account.user = user
            account.date_registraton = datetime.datetime.now()
            account.save()

        except Exception as e:
            return e
        else:
            return True
            
    def LogoutUser(self, request):
        logout(request)


