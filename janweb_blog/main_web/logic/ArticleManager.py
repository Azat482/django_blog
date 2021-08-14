from os import WIFSTOPPED
from django import conf, forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.postgres import search
from django.db.models import query_utils
from django.db.models.query import QuerySet
from django.http import request
from django.utils.datetime_safe import date
from django.conf import settings
from ..models import Article, Category
from django.contrib.postgres.search import SearchVector
from itertools import chain
import os
import datetime


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
        self.date_post = Art.data_post
        self.time_post = Art.time_post
        self.changed_flag = Art.changed_flag
    
        

class FullArticleBox(BaseArticleBox):
    def __init__(self, Art):
        self.text = Art.text
        super().__init__(Art)
    def SetDataField(data):
        pass

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
        return False
    else:
        return True


def FilterArticles(filters = {}):
    articles = None
    if filters['str'] or filters['cat'] or filters['date_from'] or filters['date_to'] or filters['user']:        
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
        
        if filters['user']:
            qs_user = Article.objects.filter(author = filters['user'])
            filter_list.append(qs_user)

        articles = QuerySet.intersection(*filter_list)
    else:
        articles = Article.objects.all()
    return articles

def GetArtcles(filters = {}):
    filters['user'] = False
    articles = FilterArticles(filters)
    toSendData = [BaseArticleBox(item) for item in articles]
    return toSendData

def GetFullPost(PostId):
    post = Article.objects.get(pk = PostId)
    return FullArticleBox(post)

def GetCat():
    CatList= Category.objects.all()
    result = [row.cat for row in CatList]
    return result

def GetUserArticles(filters = {}):
    user_articles = FilterArticles(filters)
    return [BaseArticleBox(item) for item in user_articles]

def GetSingleArticle(user, post_id):
    try:
        art = Article.objects.get(author = user, id = post_id)
        return FullArticleBox(art)
    except Exception as e:
        return False
def DeletePost(user, post_id):
    try:
        post = Article.objects.get(author = user, id = post_id)
        post_name = post.name
        post.delete()
    except Exception as e:
        print(e)
        return False        
    else:
        print(
            'Post deleted.\n',
            'Name: {0}\n'.format(post_name),
            'ID: {0}\n'.format(post_id)
        )
        return True

def EditPost(user, post_id, newdata):
    print('ID POST IN LOGIC MODULE!!!', post_id, user, newdata)
    try:
        post = Article.objects.get(author = user, id = post_id)
        post.name = newdata['name']
        post.short_description = newdata['short_description']
        post.text = newdata['text']
        post.changed_flag = True
        post.data_post = datetime.date.today()
        post.time_post = datetime.datetime.now().time()
        post.cat.remove(*Category.objects.all())
        post.cat.add(Category.objects.get(cat = newdata['category']))
        post.save()
        return True
    except Exception as e:
        print(e) 
        return False

def UploadUserImage(user, image):
    try:
        media_root = settings.MEDIA_ROOT
        media_url = 'media/'
        us_path = 'users-media/images/users-articles/' + str(user)
        datetime_str = str(datetime.datetime.now()).replace(" ", "")
        ext_img = os.path.splitext(image.name)[1] #расширение типа png jpg...
        
        full_path = "%s/%s" % (media_root, us_path)
        if not os.path.exists(full_path):
            print(full_path, ' - is not exist')
            os.makedirs(full_path)
        
        image_path = "%s/image_%s%s" % (us_path, datetime_str, ext_img)
        
        save_img_path = "%s/%s" % (media_root, image_path)
        with open(save_img_path, 'wb+') as dest:
            for small_part in image:
                dest.write(small_part)
        
        media_url_image = media_url + image_path
        return media_url_image
    except Exception as e:
        print(e)
        return False