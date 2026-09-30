from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Movie, MovieFavorite, MovieWatched
from django.core.paginator import Paginator

def home(request):
    movies = Movie.objects.all()

    paginator = Paginator(movies, 4)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    popular_movies = Movie.objects.all()[:5]

    return render(
        request,
        "movies/home.html",
        {
            "page_obj": page_obj,
            "popular_movies": popular_movies,
        },
    )


def detail(request, movie_id):
    movie = get_object_or_404(
        Movie,
        id=movie_id,
    )

    related_movies = Movie.objects.filter(
        genre=movie.genre,
    ).exclude(
        id=movie.id,
    )[:4]

    is_favorite = False
    is_watched = False

    if request.user.is_authenticated:
        is_favorite = MovieFavorite.objects.filter(
            user=request.user,
            movie=movie,
        ).exists()

        is_watched = MovieWatched.objects.filter(
            user=request.user,
            movie=movie,
        ).exists()

    return render(
        request,
        "movies/detail.html",
        {
            "movie": movie,
            "related_movies": related_movies,
            "is_favorite": is_favorite,
            "is_watched": is_watched,
        },
    )


@login_required
def toggle_favorite(request, movie_id):
    movie = get_object_or_404(
        Movie,
        id=movie_id,
    )

    favorite, created = MovieFavorite.objects.get_or_create(
        user=request.user,
        movie=movie,
    )

    if not created:
        favorite.delete()

    return redirect("movies:detail", movie_id=movie.id)


@login_required
def toggle_watched(request, movie_id):
    movie = get_object_or_404(
        Movie,
        id=movie_id,
    )

    watched, created = MovieWatched.objects.get_or_create(
        user=request.user,
        movie=movie,
    )

    if not created:
        watched.delete()

    return redirect("movies:detail", movie_id=movie.id)