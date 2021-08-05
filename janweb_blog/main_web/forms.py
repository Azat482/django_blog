from django import forms
from django.contrib.auth import validators
from django.forms import widgets
from django.forms.fields import CharField, ChoiceField
from .models import Category
from .logic.ArticleManager import GetCat
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re

class User_reg_form(forms.Form):
    login = forms.CharField(label='Your login')
    password = forms.CharField(label= 'Enter password', widget = forms.PasswordInput())
    password_again = forms.CharField(label='Enter password again', widget=forms.PasswordInput())
    email = forms.CharField(label='Enter your email')


class User_auth_form(forms.Form):
    user_login = forms.CharField(label='Your login')
    user_password = forms.CharField(label='Your pasword', widget=forms.PasswordInput())

class UserPostArticleForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #ГЕНИЙ МЫСЛИ
    name = forms.CharField(
        min_length=1,
        max_length=255,
        label='Name of article',
        widget=forms.widgets.Textarea()
        )
    
    category = forms.ChoiceField(
        choices = GetCat,
        widget= forms.Select(attrs={'class': 'select_cat'})
        )

    short_description = forms.CharField(
        min_length=1,
        max_length=500, 
        widget=forms.widgets.Textarea(),
        label='Short description of article'
        )
    

    text =  forms.CharField(
        widget=forms.widgets.Textarea(), 
        min_length=1,
        max_length=10000,
        label='Full text of article'
        )

class FilterPostsForm(forms.Form):
    
    class MyDateInput(forms.DateInput):
        input_type = 'date'
        format = '%Y-%m-%d'

    cat_filter = forms.ChoiceField(
        label='Category',
        choices=GetCat,
        widget=forms.Select(attrs={'class': 'select_cat'}), 
        required=False,
        
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
            'class': 'form-control'
           })
        )

    date_to_filter   = forms.DateField(
        required=False,
        label='To date',
        widget=MyDateInput({
            'class': 'form-control'
           })
        )



