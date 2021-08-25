import json
from django import http
from django.db.models.query import prefetch_related_objects
from django.http import response
from django.http.response import Http404, JsonResponse
from .models import Article, Category
from django import forms
from django.forms.fields import ChoiceField
from .forms import User_reg_form, User_auth_form, UserPostArticleForm, FilterPostsForm, CommentForm
from django.conf import settings

from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request, Http404

from .logic.UserMng import SiteUserManager
from .logic.ArticleManager import AddPost, GetArtcles, GetFullPost, GetUserArticles, DeletePost, EditPost, GetSingleArticle, SetPostRatingsItem
from .logic.ArticleManager import UploadUserImage, AddCommentToArticle,  GetArticleComments, GetArticleRating, SetPostRatingsItem
from .logic.SiteUserPrifileMng import ProfileDataManage


def SetUserData(req, data): #to authenticated users
    data['is_auth'] = req.user.is_authenticated
    if data['is_auth']:
        data['user'] = req.user
        profile_img = settings.SITE_URL + str(ProfileDataManage(req).GetProfileAvatar())
        data['profile_img'] = profile_img
    return data
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
        FilterForm = FilterPostsForm(field_order=['str_filter', 'cat_filter', "date_from_filter", 'date_to_filter']),
    )

    data = SetUserData(request, data)
    return render(request, 'index.html', context=data)

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
                is_reg = SiteUserManager().AddUser(data)
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
            is_auth = SiteUserManager().AuthUser(request, data)
            if is_auth:
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/login/wrong/')
    else:
        return render(request, 'login.html', {'form': User_auth_form})

def LoginingWrong(request):
    return render(request,'login.html', {'is_wrong': True, 'form': User_auth_form})

def Logout(request):
    SiteUserManager().LogoutUser(request)
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
                print('INVALID DATA')
                return HttpResponseRedirect('/addpost')
        else:
            data = dict()
            data['ArticlePost'] = UserPostArticleForm()
            data = SetUserData(request, data)
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
        data = SetUserData(request, data)
        data['comment_form'] = CommentForm()
        
        comments = GetArticleComments(idPost)
        if comments:
            data['comments'] = comments
        else:
            data["comments"] = None

        return render(request, 'fullpost_page.html', context=data)
    
def MyPosts(request):
    auth_user = request.user.is_authenticated
    if auth_user:
        data = dict(
            user_articles = GetUserArticles(
                user = request.user,
                filters = dict(
                    str = request.GET.get('str_filter', False),
                    cat = request.GET.get('cat_filter', False),
                    date_from = request.GET.get('date_from_filter', False),
                    date_to = request.GET.get('date_to_filter', False) 
                )
            ),
            filter_form = FilterPostsForm(field_order=['str_filter', 'cat_filter', "date_from_filter", 'date_to_filter']),
        )
        data = SetUserData(request, data)
        return render(request, 'user_posts_page.html', context=data)
    else:
        HttpResponseRedirect('/')


@login_required
def EditPostsReq(request):
    user = request.user
    if request.method == 'POST':
        form = UserPostArticleForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            post_id = request.POST.get('post_id')
            is_edit = EditPost(user= user,post_id= post_id, newdata= form_data)
            if is_edit:
                return HttpResponseRedirect('/myposts')
            else:
                return HttpResponseRedirect('/myposts')
        else:
            return render(request, 'poste_article.html', {'error': 'artcile is not edited'})
    else:
        id_post = request.GET.get('post_id', '')
        post_data = GetSingleArticle(user = user, post_id = id_post)
        if post_data:
            set_data_form = dict(
                name = post_data.name,
                category = post_data.cat,
                short_description = post_data.shrt_desc,
                text = post_data.text,
            )
            form = UserPostArticleForm(initial = set_data_form)
            data = dict()
            data['ArticlePost'] = form
            data['post_id_to_edit'] = id_post
            data = SetUserData(request, data)
            return render(request, 'poste_article.html', context=data)
        else:
            return HttpResponseRedirect('/myposts')


@login_required
def DeletePostReq(request):
    id_post = request.GET.get('post_id', '')
    user = request.user
    res_db = DeletePost(user, id_post)
    data = dict()
    if res_db:
        data['result'] = 'deleted succes, post id: {0}'.format(id_post)
    else:
        data['result'] = 'deleted error, post id: {0}'.format(id_post)
    return JsonResponse(data)


def AddUserImageReq(request):
    if request.user.is_authenticated:
        user = request.user
        image = request.FILES['image']
        load_image = UploadUserImage(user, image)
        print('LOAD IMAGE: ', load_image)
        if load_image:
            img_path = 'http://localhost:8000/' + load_image
            ajax_res = {
            "success": True, 
                "file": img_path,
            }
            return JsonResponse(ajax_res)
        else:
            return JsonResponse({"success": False,})
    else:
        return HttpResponseRedirect('/')


@login_required
def AccountPage(request):
    site_url = settings.SITE_URL
    ProfileMng = ProfileDataManage(request)
    ProfileMng.UpdateStatistic() 
    ProfileData = ProfileMng.GetProfileData()
    ProfileData.avatar_url = str(site_url) + str(ProfileData.avatar_url)
    data = dict(
        Profile = ProfileData,
        is_auth = request.user.is_authenticated,
    )
    data = SetUserData(request, data)
    print('Profile data: ', data['Profile'])
    return render(request, 'user_profile.html', context=data)


@login_required
def AccountSetAvatarReq(request):
    if request.method == 'POST':
        img = request.FILES['avatar']
        upload_ava = ProfileDataManage(request).SetAvatarProfile(img)
        return HttpResponseRedirect('./')

@login_required
def CommentArticleReq(request):
    user = request.user
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        form_data = comment_form.cleaned_data
        post_id = request.POST.get('post_id', None)
        text = form_data['comment_text']
        comment_is_added = AddCommentToArticle(user, text, post_id)
        print('comment is added: ', comment_is_added)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def GetPostRatingsReq(request):
    try:
        post_id = request.GET.get('post_id', None)
        print('GET POST ID:', post_id)
        post_ratings = GetArticleRating(post_id)
        if post_ratings:
            return JsonResponse(post_ratings)
        else:
            raise
    except:
        return JsonResponse({
                "err": "error server",
            })


@login_required
def SetUserRatingToPostReq(request):
    method =  request.GET.get('method', None)
    post_id = request.GET.get('post_id', None)
    user = request.user
    result_setting = SetPostRatingsItem(user, post_id, method)
    if result_setting:
        return JsonResponse({
            "res": "set success"
        })
    else:
        return JsonResponse({
                "res": 'error',
        })