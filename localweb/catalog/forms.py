from django import forms
from catalog.choices import *
from django.core.validators import RegexValidator


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': ''}))
    password = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class RegisterForm(forms.Form):
    #regular expression constraint + username&password
    regex_phone = r'^1[34578]\d{9}$'
    regex_personal_ID = r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$'
    regex_username = r'^[a-z0-9_-]{3,16}$'
    regex_password = r'^[a-z0-9_-]{6,18}$'
    phone_validator = RegexValidator(regex=regex_phone, message='手机号格式错误')
    personal_ID_validator = RegexValidator(regex=regex_personal_ID, message='身份证非法输入')
    username_validator = RegexValidator(regex=regex_username, message='用户名非法')
    password_validator = RegexValidator(regex=regex_password, message='密码非法')
    
    username = forms.CharField(label='用户名', max_length=128, validators=[username_validator], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': ''}))
    password = forms.CharField(label='密码', max_length=256, validators=[password_validator], widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_pw = forms.CharField(label='确认密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    sex = forms.ChoiceField(label='性别', choices=gender, widget=forms.Select())
    last_name = forms.CharField(label='姓', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    first_name = forms.CharField(label='名', max_length=
    128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    birth = forms.DateField(label='出生日期', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': '2000-01-01'}))
    email = forms.EmailField(label='邮箱', max_length=128, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
    phone = forms.CharField(label='手机号', max_length=128, validators=[phone_validator], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    personal_ID = forms.CharField(label='身份证', max_length=128, validators=[personal_ID_validator], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Personal ID'}))
    role = forms.ChoiceField(label='身份', choices=account_types, widget=forms.Select())


class IndexForm(forms.Form):
    rest_search = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '搜索商家', 'style': 'width: 250px;'}))


class RestaurantForm(forms.Form):
    rest_name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '商家名称'}))