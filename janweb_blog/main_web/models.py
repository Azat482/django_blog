from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    
    cat = models.CharField(max_length=50)

class Article(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    cat = models.ManyToManyField(Category)
    short_description = models.CharField(max_length=500, default='')
    text = models.TextField(max_length=10000)
    data_post = models.DateField(null=True, auto_now= False, auto_now_add=False)
    time_post = models.TimeField(null=True, auto_now_add=False, auto_now=False)
