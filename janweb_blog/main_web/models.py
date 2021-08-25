from django.db import models
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime


class BaseSiteContentObject(models.Model):
    class Meta:
        abstract = True

#Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE, primary_key=True)
    avatar_url = models.ImageField(max_length = 200, null=True)
    date_registration = models.DateTimeField(auto_now_add=True) 
    user_likes_count = models.IntegerField(default=0, null=False)
    user_dislikes_count = models.IntegerField(default=0, null=False)
    user_articles_count = models.IntegerField(default=0, null= False)
    user_comments_count = models.IntegerField(default=0, null =False)
    

class Category(models.Model):
    cat = models.CharField(max_length=50)


class Article(BaseSiteContentObject):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    cat = models.ManyToManyField(Category)
    short_description = models.CharField(max_length=500, default='')
    text = models.TextField(max_length=200000)
    data_post = models.DateField(null=True, auto_now= False, auto_now_add=False)
    time_post = models.TimeField(null=True, auto_now_add=False, auto_now=False)
    changed_flag = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-data_post', '-time_post']


class BaseContentAttributes(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    datetime_creating = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-datetime_creating']
        
        abstract = True

class CommentContent(BaseContentAttributes):
    comment_text = models.TextField(max_length=5000, null=True)
    class Meta(BaseContentAttributes.Meta):
        abstract = True

class LikeContent(BaseContentAttributes):
    class Meta(BaseContentAttributes.Meta):
        abstract = True

class DislikeContent(BaseContentAttributes):
    class Meta(BaseContentAttributes.Meta):
        abstract = True

#function are added for each entity 

#to articles
class CommentArticle(CommentContent):
    owner_object = models.ForeignKey(Article, null=True, on_delete=models.CASCADE)
    
class LikeArticle(LikeContent):
    owner_object = models.ForeignKey(Article, null=True, on_delete=models.CASCADE)
    class Meta:
        unique_together = ['user', 'owner_object']

class DislikeArticle(DislikeContent):
    owner_object = models.ForeignKey(Article, null=True, on_delete=models.CASCADE)
    class Meta:
        unique_together = ['user', 'owner_object']

#to comments
class LikeArticleComment(LikeContent):
    owner_object = models.ForeignKey(CommentArticle, null=True, on_delete=models.CASCADE)
    class Meta:
        unique_together = ['user', 'owner_object']

class DislikeArticleComment(DislikeContent):
    owner_object = models.ForeignKey(CommentArticle, null=True, on_delete=models.CASCADE)
    class Meta:
        unique_together = ['user', 'owner_object']



