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

