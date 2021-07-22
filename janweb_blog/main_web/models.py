from django.db import models

# Create your models here.
class Users(models.Model):
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    privilage = models.IntegerField()

class Article(models.Model):
    author = models.ForeignKey(Users, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    cat = models.CharField(max_length=100)
    text = models.TextField()


    