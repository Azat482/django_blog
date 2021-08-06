from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.postgres import search
from django.db.models import query_utils
from django.db.models.query import QuerySet
from django.http import request
from django.utils.datetime_safe import date
from ..models import Article, Category
from django.contrib.postgres.search import SearchVector
import datetime
from itertools import chain

class BaseArticleBox:
    def __init__(self, Art):
        cat = []
        for i in Art.cat.all():
            cat.append(i.cat)
        self.author = Art.author
        self.id = Art.id
        self.name = Art.name
        self.cat = cat
        self.shrt_desc = Art.short_description

class FullArticleBox(BaseArticleBox):
    def __init__(self, Art):
        self.text = Art.text
        super().__init__(Art)

def AddPost(req, data):
    name       = data['name']
    category   = data['category'] 
    short_text = data['short_text'] 
    full_text  = data['text']
    print('cat:', category)
    article = Article()
    try:
        print(User.objects.all())
        print('username: ', req.user)
        article.author = User.objects.get(username = req.user)    
        article.name = name
        article.short_description = short_text
        article.text = full_text
        article.data_post = datetime.date.today()
        article.time_post = datetime.datetime.now().time()
        article.save()
        article.cat.add(Category.objects.get(cat = category))
    except Exception as e:
        return e
    else:
        return True

def GetArtcles(filters = {}):
    print('FILTERS:', filters)
    articles = None

    if filters['str'] or filters['cat'] or filters['date_from'] or filters['date_to']:        
        filter_list = []
        
        if filters['cat']:
            qs_cat_filter      = Article.objects.filter(cat__cat = filters['cat'])
            filter_list.append(qs_cat_filter)
        
        if filters['str']:
            qs_name_filter     = Article.objects.filter(name__search = filters['str'])
            qs_srt_desc_filter = Article.objects.filter(short_description__search = filters['str'])
            qs_text_filter     = Article.objects.filter(text__search = filters['str'])
            buff = QuerySet.union(qs_name_filter, qs_srt_desc_filter, qs_text_filter)
            filter_list.append(buff)
        
        if filters['date_from'] and not filters['date_to']:
            qs_from_date = Article.objects.filter(
                data_post__gte = filters['date_from']
                )
            filter_list.append(qs_from_date)

        if filters['date_to'] and not filters['date_from']:
            qs_to_date = Article.objects.filter(
                data_post__lte = filters['date_to']
                )
            filter_list.append(qs_to_date)

        if filters['date_from'] and filters['date_to']:
            qs_from_to_date = Article.objects.filter(
                data_post__range = (filters['date_from'], filters['date_to'])
                )
            filter_list.append(qs_from_to_date)

        articles = QuerySet.intersection(*filter_list)
    else:
        articles = Article.objects.all()

    toSendData = [BaseArticleBox(item) for item in articles]
    return toSendData

def GetFullPost(PostId):
    post = Article.objects.get(pk = PostId)
    return FullArticleBox(post)

def GetCat():
    CatList= Category.objects.all()
    result = [row.cat for row in CatList]
    return result