from django import forms
from django.contrib import auth
from django.contrib.auth import login
from django.forms.fields import ChoiceField
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request
from .forms import User_reg_form, User_auth_form, UserPostArticleForm
from .logic.UserMng import AddUser, AuthUser, LogoutUser
from .logic.ArticlePost import AddPost

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        print('req', request)
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
                if is_reg == True:
                    return HttpResponseRedirect('/login')
                else:
                    err = '?error=' + str(is_reg)
                    return HttpResponseRedirect('/registration' + err)
    else:
        err = request.GET.get('error', None)
        return render(request, 'registration.html', {'form' : User_reg_form, 'error': err})

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

def PosteArticle(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UserPostArticleForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                post_data = dict()
                post_data['name'] = data['name']
                post_data['short_text'] = data['short_description']
                post_data['text'] = data['text']
                post_data['category'] = data['category']
                result = AddPost(request, post_data)
                if result == True:
                    return HttpResponseRedirect('/')
                else:
                    print('ERROR', result)
                    return HttpResponseRedirect('/poste')
        else:
            data = dict()
            data['ArticlePost'] = UserPostArticleForm()
            return render(request, 'poste_article.html', context=data)
    else:
        return HttpResponseRedirect('/')