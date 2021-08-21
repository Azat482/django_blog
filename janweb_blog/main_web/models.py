from os import truncate
from typing import Text
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils.datetime_safe import datetime

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE, primary_key=True)
    avatar_url = models.ImageField(max_length = 200, null=True)
    date_registration = models.DateTimeField(auto_now_add=True) 
    user_likes_count = models.IntegerField(default=0, null=False)
    user_diselikes_count = models.IntegerField(default=0, null=False)
    user_articles_count = models.IntegerField(default=0, null= False)
    user_comments_count = models.IntegerField(default=0, null =False)

class Category(models.Model):
    cat = models.CharField(max_length=50)


class Comment(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    comment = models.TextField(max_length=5000, null=False)
    datetime = models.DateTimeField(auto_now_add=True)


class Article(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    cat = models.ManyToManyField(Category)
    short_description = models.CharField(max_length=500, default='')
    text = models.TextField(max_length=200000)
    data_post = models.DateField(null=True, auto_now= False, auto_now_add=False)
    time_post = models.TimeField(null=True, auto_now_add=False, auto_now=False)
    changed_flag = models.BooleanField(default=False)
    comments = models.ForeignKey(Comment, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-data_post']

