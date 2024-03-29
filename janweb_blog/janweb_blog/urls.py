"""janweb_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path, re_path
from main_web import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),

    #reg and auth
    path('registration/', views.Registration),
    path('login/', views.Logining),
    path('logout/', views.Logout),
    path('login/wrong/', views.LoginingWrong),
    path('account/set-avatar', views.AccountSetAvatarReq),
    re_path(r'^account/', views.AccountPage),

    path('addpost/', views.PosteArticle),
    path('myposts/', views.MyPosts),
    path('post/', views.GetPost, name='full_post'),
    path('myposts/delete_post', views.DeletePostReq,  name='delete_post'),
    path('myposts/edit_user_post', views.EditPostsReq, name='edit_post'),
    path('addimage/', views.AddUserImageReq, name='add_image'),
    path('comment/post/', views.CommentArticleReq, name='comment_article'),
    path('get_post_ratings/', views.GetPostRatingsReq, name='get_post_ratings'),    
    path('set_user_rating_to_post/', views.SetUserRatingToPostReq, name = 'set_user_rating_to_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   
