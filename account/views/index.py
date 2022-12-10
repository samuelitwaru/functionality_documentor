from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from ..forms import LoginForm, SignupForm


def index(request):
    # if logged in: redirect to get_apps
    if get_user(request).is_authenticated:
        return redirect('core:get_apps')
    # else: redirect to signin view
    else:
        return redirect('account:signin')


def signin(request):
    _next = request.GET.get("next", "core:get_apps")
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect(_next)
        else:
            messages.error(request, f"User not found!", extra_tags="danger")
            return redirect("account:signin")
    else:
        if get_user(request).is_authenticated:
            return redirect('core:get_apps')
        login_form = LoginForm()
        context = {"login_form": login_form}
        return render(request, 'index/signin.html', context)


def signup(request):
    if request.method == "POST":
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid:
            data = request.POST
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            username = data['username']
            password = data['password']
            user = User(first_name=first_name, last_name=last_name,
                        username=username, email=email)
            user.set_password(password)
            user.save()
            messages.success(request, "User created", "success")
            return redirect('account:index')
    else:
        signup_form = SignupForm()

    context = {'signup_form': signup_form}
    return render(request, 'index/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('account:index')
