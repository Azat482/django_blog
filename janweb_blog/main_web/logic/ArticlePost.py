from django.contrib.auth.models import User
from django.http import request
from ..models import Article, Category

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