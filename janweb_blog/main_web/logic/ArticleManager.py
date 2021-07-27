from django.contrib import auth
from django.contrib.auth.models import User
from django.http import request
from ..models import Article, Category

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
        article.save()
        article.cat.add(Category.objects.get(cat = category))
    except Exception as e:
        return e
    else:
        return True

def GetArtcles(filters = None):
    toSendData = []
    for item in Article.objects.all():
        toSendData.append(BaseArticleBox(item))
    return toSendData

def GetFullPost(PostId):
    post = Article.objects.get(pk = PostId)
    return FullArticleBox(post)


                
        

