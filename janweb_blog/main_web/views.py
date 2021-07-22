from django.contrib import auth
from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request
from .forms import User_reg_form, User_auth_form
from .logic.UserMng import AddUser, AuthUser, LogoutUser

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'ex_auth_index.html' )

def Registration(request):
    if request.method == 'POST':
        reg_form = User_reg_form(request.POST)
        if reg_form.is_valid():
            data = dict()
            data['username'] = reg_form.cleaned_data['login']
            data['password'] = reg_form.cleaned_data['password']
            data['password_again'] = reg_form.cleaned_data['password_again']
            data['email'] = reg_form.cleaned_data['email']
            if data['password'] == data['password_again']:
                is_reg = AddUser(data)
                if is_reg:
                    return HttpResponseRedirect('/login')

    else:
        return render(request, 'registration.html', {'form' : User_reg_form})

    return render(request, 'registration.html')

def Logining(request):
    if request.method == 'POST':
        log_form = User_auth_form(request.POST)
        if log_form.is_valid():
            data = dict()
            data['username'] = log_form.cleaned_data['user_login']
            data['password'] = log_form.cleaned_data['user_password']
            is_auth = AuthUser(request, data)
            if is_auth:
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/login/wrong/')
    else:
        return render(request, 'login.html', {'form': User_auth_form})

def LoginingWrong(request):
    return render(request,'login.html', {'is_wrong': True, 'form': User_auth_form})

def Logout(request):
    LogoutUser(request)
    return HttpResponseRedirect('/')