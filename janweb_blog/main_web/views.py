from django.http.response import Http404
from .models import Article
from django import forms
from django.forms.fields import ChoiceField
from .forms import User_reg_form, User_auth_form, UserPostArticleForm, FilterPostsForm

from django.contrib import auth
from django.contrib.auth import login

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request, Http404

from .logic.UserMng import AddUser, AuthUser, LogoutUser
from .logic.ArticleManager import AddPost, GetArtcles, GetFullPost

# Create your views here.
def index(request):
    data = dict(
        articles = GetArtcles(
            filters = dict(
                str  = request.GET.get('str_filter', False),
                cat  = request.GET.get('cat_filter', False),
                date_from = request.GET.get('date_from_filter', False),
                date_to = request.GET.get('date_to_filter', False),
            )
        ),
        FilterForm = FilterPostsForm(),
    )
    if not request.user.is_authenticated:
        return render(request, 'index.html', context=data)
    else:
        print('req', request)
        return render(request, 'ex_auth_index.html', context = data )

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
                    print('ERROR!!!:', result)
                    return HttpResponseRedirect('/addpost')
        else:
            data = dict()
            data['ArticlePost'] = UserPostArticleForm()
            return render(request, 'poste_article.html', context=data)
    else:
        return HttpResponseRedirect('/')

def GetPost(request):
    idPost = request.GET.get('id')
    try:
        post = GetFullPost(idPost)
    except Exception as e:
        print(e)
        raise Http404
    else:
        data = dict()
        data['post'] = post
        if request.user.is_authenticated:
            data['is_auth'] = True
            print(data['is_auth'])
        else: 
            data['is_auth'] = False
        return render(request, 'fullpost_page.html', context=data)
    