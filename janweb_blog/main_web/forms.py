from django import forms
from django.forms import widgets
from django.forms.fields import CharField, ChoiceField
from .models import Category

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
    def GetCat():
        CatList= Category.objects.all()
        result = []
        for row in CatList:
            result.append( (row.cat, row.cat) )
        return result

    name = forms.CharField(
        min_length=1,
        max_length=255,
        label='Name of article',
        widget=forms.widgets.Textarea()
        )
    
    category = forms.ChoiceField(
        choices = GetCat,
        widget= forms.Select(attrs={'id': 'select_cat'})
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

