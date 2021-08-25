from django import forms, setup
from django.contrib.auth import validators
from django.db import models
from django.forms import widgets
from django.forms.fields import CharField, ChoiceField
from .models import Category
from .logic.ArticleManager import GetCat
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from itertools import chain

class User_reg_form(forms.Form):
    login = forms.CharField(label='Your login')
    password = forms.CharField(label= 'Enter password', widget = forms.PasswordInput())
    password_again = forms.CharField(label='Enter password again', widget=forms.PasswordInput())
    email = forms.CharField(label='Enter your email')


class User_auth_form(forms.Form):
    user_login = forms.CharField(label='Your login')
    user_password = forms.CharField(label='Your pasword', widget=forms.PasswordInput())

#да, я знаю, что можно было создать форму на основе модели
class UserPostArticleForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def CreateCatList(cats):
        return [(cat, cat) for cat in cats]
    #ГЕНИЙ МЫСЛИ
    name = forms.CharField(
        min_length=10,
        max_length=255,
        label='Name of article',
        widget=forms.widgets.Textarea()
        )
    
    category = forms.ChoiceField(
        choices = CreateCatList(GetCat()),
        widget= forms.Select(attrs={'class': 'select_cat'})
        )

    short_description = forms.CharField(
        min_length=100,
        max_length=500, 
        widget=forms.widgets.Textarea(),
        label='Short description of article'
        )
    

    text =  forms.CharField(
        widget=forms.widgets.Textarea(attrs={'id': 'article_text'}), 
        min_length=1000,
        max_length=200000,
        label='Full text of article'
        )

class FilterPostsForm(forms.Form):
    
    def CreateCatList( cats):
        default_selec = 'all category'
        rez = [(cat, cat) for cat in cats]
        rez.insert(0, (None, default_selec))
        return rez

    class MyDateInput(forms.DateInput):
        input_type = 'date'
        format = '%Y-%m-%d'

    cat_filter = forms.ChoiceField(
        label='Category',
        widget=forms.Select(attrs={'class': 'select_cat' }), 
        required=False,
        choices = CreateCatList( GetCat())
    )

    str_filter = forms.CharField(
        label='Articles witch contains',
        min_length=1,
        max_length=100,
        widget = forms.TextInput(attrs={'class': 'search_field'}),
        required=False,
    )

    date_from_filter = forms.DateField(
        required = False,
        label='From date',
        widget=MyDateInput({
            'class': 'form-control date_field'
           })
        )

    date_to_filter   = forms.DateField(
        required=False,
        label='To date',
        widget=MyDateInput({
            'class': 'form-control date_field'
           })
        )


class CommentForm(forms.Form):
    comment_text = forms.CharField(
        required=True,
        max_length=5000,
        min_length=5,
        label='Your comment',
        widget=forms.widgets.Textarea(attrs={'class': 'comment_form_text'}),
    )
