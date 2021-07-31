from django import forms
from django.contrib.auth import validators
from django.forms import widgets
from django.forms.fields import CharField, ChoiceField
from .models import Category
from .logic.ArticleManager import GetCat
from django.core.validators import RegexValidator

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
    DATA_FORMAT_VALIDATOR = RegexValidator(r'^\\d{2}\\.\\d{2}\\.\\d{4}$', 'wrong format of data')
    cat_filter = forms.ChoiceField(
        label='category',
        choices=GetCat,
        widget=forms.Select(attrs={'class': 'select_cat'}), 
        required=False
    )

    str_filter = forms.CharField(
        label='articles witch contains',
        min_length=1,
        max_length=100,
        widget = forms.TextInput(attrs={'class': 'search_field'}),
        required=False,
    )

    data_from = forms.CharField(
        initial='dd/mm/yy',
        required=False,
        label='from date',
        validators=[DATA_FORMAT_VALIDATOR],
        )

    data_to   = forms.CharField(
        initial='dd/mm/yy',
        required=False,
        label='to date',
        validators=[DATA_FORMAT_VALIDATOR],
        )



