from django import forms
from app.models import UserProfileInfo
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput())

    class Meta:

        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    # 'label': "Password"
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class UserProfileInfoForm(forms.ModelForm):

    class Meta:

        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')
        widgets = {
            'portfolio_site': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            # 'profile_pic': forms.FileInput(
            #     attrs={
            #         'class': 'form-control',
            #     }
            # )

        }


class LoginForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'id': "PasswordId",
                    'min': 3
                    # 'label': "Password"
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class UserProfileForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput())
    # password = forms.CharField(widget=forms.PasswordInput(), required=True)
    # password_1 = forms.CharField(widget=forms.PasswordInput(attrs={
    #                 'class': 'form-control',
    #             }), required=True, label='Confirm password', )

    class Meta:

        model = User
        fields = ('id', 'first_name', 'last_name', 'email', )#'__all__'  #  'password'
        widgets = {
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    # 'label': "Password"
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'id': forms.TextInput(
                attrs={
                    'type': 'hidden',
                    'class': 'form-control'
                }
            ),
        }
        # exclude = ['username', 'password']
        # attrs = {'class': 'form-control'}
        parsley_extras = {
            'password_1': {
                'equalto': "password",
                'error-message': "Your passwords do not match.",
            },
        }
