from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class ProfileCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(label='Username, Email or Phone')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
