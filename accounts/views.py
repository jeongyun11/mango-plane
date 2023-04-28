from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


def login(request):
    if request.user.is_authenticated:
        return redirect('spots:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('spots:index')
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('spots:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('spots:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('spots:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

@login_required
def profile(request):
    user = request.user
    spots = user.spot_set.all()
    context = {
        'spots': spots,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('reviews:index')