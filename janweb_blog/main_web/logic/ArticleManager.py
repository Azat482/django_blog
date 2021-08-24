from django import conf, forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.postgres import search
from django.db.models import query_utils
from django.db.models.query import QuerySet
from django.http import request
from django.utils.datetime_safe import date
from django.conf import settings
from ..models import Article, Category, CommentArticle, LikeArticle, DislikeArticle
from django.contrib.postgres.search import SearchVector
from itertools import chain
import os
import datetime
from .FileManager import FileManager
from .UserActionsManager import UserActionsManager

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

class ArticleCommentBox:
    def __init__(self, comment):
        self.user = comment.user
        self.pub_datetime = comment.datetime_creating
        self.text = comment.comment_text


def AddPost(req, data):
    name       = data['name']
    category   = data['category'] 
    short_text = data['short_text'] 
    full_text  = data['text']
    print('cat:', category)
    article = Article()
    try:
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


def FilterArticles(Articles, filters = {}):
    articles = None
    if filters['str'] or filters['cat'] or filters['date_from'] or filters['date_to']:        
        filter_list = []
        
        if filters['cat']:
            qs_cat_filter      = Articles.filter(cat__cat = filters['cat'])
            filter_list.append(qs_cat_filter)
        
        if filters['str']:
            qs_name_filter     = Articles.filter(name__search = filters['str'])
            qs_srt_desc_filter = Articles.filter(short_description__search = filters['str'])
            qs_text_filter     = Articles.filter(text__search = filters['str'])
            buff = QuerySet.union(qs_name_filter, qs_srt_desc_filter, qs_text_filter)
            filter_list.append(buff)
        
        if filters['date_from'] and not filters['date_to']:
            qs_from_date = Articles.filter(
                data_post__gte = filters['date_from']
                )
            filter_list.append(qs_from_date)

        if filters['date_to'] and not filters['date_from']:
            qs_to_date = Articles.filter(
                data_post__lte = filters['date_to']
                )
            filter_list.append(qs_to_date)

        if filters['date_from'] and filters['date_to']:
            qs_from_to_date = Articles.filter(
                data_post__range = (filters['date_from'], filters['date_to'])
                )
            filter_list.append(qs_from_to_date)

        articles = QuerySet.intersection(*filter_list)
    else:
        articles = Articles
    return articles

def GetArtcles(filters = {}):
    articles = FilterArticles(Article.objects.all(), filters)
    toSendData = [BaseArticleBox(item) for item in articles]
    return toSendData

def GetFullPost(PostId):
    post = Article.objects.get(pk = PostId)
    return FullArticleBox(post)

def GetCat():
    CatList= Category.objects.all()
    result = [row.cat for row in CatList]
    return result

def GetUserArticles(user, filters = {}):
    user_articles = FilterArticles(user.article_set.all(), filters)
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
        path = 'users-media/images/users-articles/' + str(user)
        exeption = os.path.splitext(image.name)[1]
        name = ("_image%s%s" % (str(datetime.datetime.now()), exeption)).replace(' ', '')
        upload = FileManager().UploadMediaFile(image, path, name)
        print('IMAGE PATH GETTING FROM UPLOADER: ', upload)
        return upload
    except Exception as e:
        print('SETAVAERR: ', e)
        return False



def AddCommentToArticle(user, text, post_id):
    UserAction = UserActionsManager(user)
    result_action = UserAction.AddCommentToObject(
        CommentModel = CommentArticle,
        OwnerObject = Article,
        text = text,
        obj_id =post_id 
    )
    return result_action

def GetArticleComments(post_id):
    try:
        comments_qs = Article.objects.get(id = post_id).commentarticle_set.all()
        comments = [ArticleCommentBox(item) for item in comments_qs]
        return comments
    except Exception as e:
        print(e)
        return False

def GetArticleRating(post_id):
    try:
        article = Article.objects.get(id = post_id)
        rating_post = {
            "likes": article.likearticle_set.all().count(),
            "dislikes": article.dislikearticle_set.all().count(),
        }
        return rating_post
    except Exception as e:
        print(e)
        return False

def SetPostRatingsItem(user, post_id, method):
    UserAction = UserActionsManager(user)
    result_action = UserAction.SetRatingItemToObject(
        LikeModel = LikeArticle,
        DislikeModel = DislikeArticle,
        OwnerObject = Article,
        method= method, 
        obj_id= post_id
        )
    return result_action