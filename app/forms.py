from django import forms
from app.models import UserProfileInfo
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:

        model = User
        fields = ('username', 'password', 'email')
        attrs = {'class': 'form-control'}


class UserProfileInfoForm(forms.ModelForm):

    class Meta:

        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')
        attrs = {'class': 'form-control'}


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']