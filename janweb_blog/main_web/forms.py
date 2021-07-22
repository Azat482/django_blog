from django import forms


class User_reg_form(forms.Form):
    login = forms.CharField(label='Your login')
    password = forms.CharField(label= 'Enter password', widget = forms.PasswordInput())
    password_again = forms.CharField(label='Enter password again', widget=forms.PasswordInput())
    email = forms.CharField(label='Enter your email')


class User_auth_form(forms.Form):
    user_login = forms.CharField(label='Your login')
    user_password = forms.CharField(label='Your pasword', widget=forms.PasswordInput())