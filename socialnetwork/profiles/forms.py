from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Profile


class ProfileCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = '__all__'


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label=_('First name'))
    last_name = forms.CharField(label=_('Last name'))
    email = forms.EmailField(label=_('Email'))
    birth_date = forms.DateField(label=_('Birth date YYYY-MM-DD'))

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date', 'gender']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError(_('Invalid first name.'))
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError(_('Invalid last name.'))
        return last_name


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username, Email or Phone'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
