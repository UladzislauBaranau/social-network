from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _


from .forms import EditAvatarUsernameBioForm, EditProfileForm, LoginForm, RegisterForm
from .models import Profile


def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('The profile has been successfully created'))

    context = {
        'form': form,
    }
    return render(request, 'profiles/register.html', context)


def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('user_profile')
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.error(request, _('The entered data is incorrect'))

    context = {
        'form': form,
    }
    return render(request, 'profiles/login.html', context)


@login_required(login_url='/profiles/login')
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/profiles/login')
def user_profile_view(request):
    profile = Profile.objects.get(id=request.user.id)
    form = EditAvatarUsernameBioForm(instance=request.user)

    if request.method == 'POST':
        form = EditAvatarUsernameBioForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your profile has been updated'))

    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'profiles/user_profile.html', context)


@login_required(login_url='/profiles/login')
def edit_profile_view(request):
    form = EditProfileForm(instance=request.user)
    confirm = False

    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/edit_profile.html', context)
