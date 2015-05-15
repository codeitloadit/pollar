from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_GET, require_POST


def home(request):
    # if request.user.is_authenticated():
    #     return HttpResponseRedirect(reverse('home'))
    # else:
    #     return HttpResponseRedirect(reverse('login_or_register'))
    return TemplateResponse(request, 'home.html')


def login_or_register(request):
    return TemplateResponse(request, 'login_or_register.html')


@require_POST
def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    confirm = request.POST.get('confirm')
    messages = []
    if not username or not password or not confirm:
        messages.append('All fields are required!')
        return TemplateResponse(request, 'login_or_register.html', {'messages': messages, 'register_tab': True})
    if password != confirm:
        messages.append('Passwords did not match!')
        return TemplateResponse(request, 'login_or_register.html', {'messages': messages, 'register_tab': True})
    try:
        User.objects.create_user(username=username, password=password)
    except IntegrityError:
        messages.append('That username is already taken!')
        return TemplateResponse(request, 'login_or_register.html', {'messages': messages, 'register_tab': True})
    user = auth.authenticate(username=username, password=password)
    auth.login(request, user)
    return TemplateResponse(request, 'home.html')


@require_POST
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('login'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('home'))
