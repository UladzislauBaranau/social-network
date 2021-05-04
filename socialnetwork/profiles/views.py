from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm


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
                    return HttpResponse('You profile')
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.error(request, 'The entered data is incorrect')

    context = {
        'form': form,
    }
    return render(request, 'profiles/login.html', context)
