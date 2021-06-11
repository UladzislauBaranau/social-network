from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from .backends import get_friends
from .forms import EditAvatarUsernameBioForm, EditProfileForm, LoginForm, RegisterForm
from .models import Friendship, Profile


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


@login_required(login_url='/profiles/login')
def export_personal_data_view(request):
    user_profile = Profile.objects.get(id=request.user.id)

    personal_data = {
        'username': user_profile.username,
        'first_name': user_profile.first_name,
        'last_name': user_profile.last_name,
        'email': user_profile.email,
        'phone': user_profile.phone,
        'birth_date': user_profile.birth_date,
        'country': user_profile.country,
        'city': user_profile.city,
    }

    response = JsonResponse(personal_data)
    response['Content-Disposition'] = "attachment; filename=personal_data_" + user_profile.username + '.json'
    return response


@login_required(login_url='/profiles/login')
def remove_account_view(request):
    account = Profile.objects.get(id=request.user.id)

    if request.method == "POST":
        account.delete()
        messages.info(request, _('Your account was successfully deleted.'))

    context = {
        'account': account,
    }
    return render(request, 'profiles/remove_account.html', context)


@login_required(login_url='/profiles/login')
def get_friends_list_view(request):
    friends = get_friends(request)

    context = {
        'friends': friends,
    }
    return render(request, 'profiles/friends_list.html', context)


@login_required(login_url='/profiles/login')
def friend_details_view(request, pk):
    obj = get_object_or_404(Profile, pk=pk)

    context = {
        'obj': obj,
    }
    return render(request, 'profiles/friend_details.html', context)


@login_required(login_url='/profiles/login')
def search_result_friends(request):
    friends = get_friends(request)

    if request.is_ajax():
        searched = request.POST.get('friend')
        matches_friends = []
        for i in friends:
            if i.first_name.lower().startswith(searched.lower()) or \
                    i.last_name.lower().startswith(searched.lower()):
                matches_friends.append(i)

        if len(matches_friends) > 0 and len(searched) > 0:
            data = []
            for pos in matches_friends:
                item = {
                    'pk': pos.pk,
                    'first_name': pos.first_name,
                    'last_name': pos.last_name,
                    'bio': pos.bio,
                    'avatar': str(pos.avatar.url),
                }
                data.append(item)
            res = data
        else:
            res = 'No friends found ...'

        return JsonResponse({'data': res})
    return JsonResponse({})


@login_required(login_url='/profiles/login')
def remove_from_friends(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        sender = Profile.objects.get(id=request.user.id)
        receiver = Profile.objects.get(pk=pk)

        qs_friendship = Friendship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender)),
        )
        qs_friendship.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('remove_friend')


@login_required(login_url='/profiles/login')
def search_users(request):
    searched_user = Profile.objects.all().exclude(id=request.user.id)

    if request.method == "POST":
        searched = request.POST['searched_users']
        searched_user = Profile.objects.filter(
            (Q(first_name__istartswith=searched)) | (Q(last_name__istartswith=searched)),
        ).exclude(id=request.user.id)

    profile = Profile.objects.get(id=request.user.id)
    qs = Friendship.objects.filter(sender=profile).filter(status='A')
    accepted = [friendship.receiver for friendship in qs]

    context = {
        'users': searched_user,
        'profile': profile,
        'accepted': accepted,
    }
    return render(request, 'profiles/searched_users.html', context)


@login_required(login_url='/profiles/login')
def send_invitation(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        sender = Profile.objects.get(id=request.user.id)
        receiver = Profile.objects.get(pk=pk)

        Friendship.objects.create(sender=sender, receiver=receiver, status='S')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('send_invitation')
