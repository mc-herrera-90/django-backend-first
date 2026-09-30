from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from movies.models import Movie
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("accounts:profile")
    else:
        form = UserLoginForm(request)

    return render(
        request,
        "registration/login.html",
        {"form": form},
    )


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("accounts:login")
    else:
        form = UserRegisterForm()

    return render(
        request,
        "registration/register.html",
        {"form": form},
    )


def logout_view(request):
    if request.method == "POST":
        logout(request)

    return redirect("accounts:login")


@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
    else:
        form = UserProfileForm(
            instance=request.user,
        )

    favorite_movies = Movie.objects.filter(
        favorites__user=request.user,
    )

    watched_movies = Movie.objects.filter(
        watched_by__user=request.user,
    )

    return render(
        request,
        "registration/profile.html",
        {
            "form": form,
            "favorite_movies": favorite_movies,
            "watched_movies": watched_movies,
        },
    )