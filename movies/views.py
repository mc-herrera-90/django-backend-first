from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

from .models import Movie


def home(request):
    movies = Movie.all()

    paginator = Paginator(movies, 4)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    popular_movies = sorted(
        movies,
        key=lambda movie: movie.rating,
        reverse=True,
    )[:5]

    return render(
        request,
        "movies/home.html",
        {
            "page_obj": page_obj,
            "popular_movies": popular_movies,
        },
    )


def detail(request, movie_id):
    movie = Movie.get(movie_id)

    if movie is None:
        raise Http404("La película no existe.")

    related_movies = sorted(
        [
            related_movie
            for related_movie in Movie.all()
            if related_movie.id != movie.id
            and related_movie.genre == movie.genre
        ],
        key=lambda movie: movie.rating,
        reverse=True,
    )[:4]

    return render(
        request,
        "movies/detail.html",
        {
            "movie": movie,
            "related_movies": related_movies,
        },
    )