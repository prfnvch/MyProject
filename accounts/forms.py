from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(required=False)
    city = forms.CharField(required=False)
    country = forms.CharField(required=False)
    instagram = forms.CharField(required=False)
    telegram = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    def clean_password2(self):
        data = self.cleaned_data

        if data['password1'] != data['password2']:
            raise forms.ValidationError('Passwords do not match')
        return data['password2']
    

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password1 = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'remember_me']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ProfileEditForm(UserChangeForm):
    username = forms.CharField()
    email = forms.CharField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)
    city = forms.CharField(required=False)
    country = forms.CharField(required=False)
    instagram = forms.CharField(required=False)
    telegram = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "avatar", "country", "city", "bio", "telegram", "instagram")
