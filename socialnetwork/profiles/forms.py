from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Profile


class ProfileCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username, Email or Phone'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
