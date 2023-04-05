from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from SocialWeb.models import Post,Comments,UserProfile

class RegistartionForm(UserCreationForm):

    class Meta:
        model=User
        fields=["username","email","password1","password2"]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=["image","description"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["profile_pic","bio"]