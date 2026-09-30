from django.urls import path

from . import views


app_name = "movies"


urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),
    path(
        "<int:movie_id>/",
        views.detail,
        name="detail",
    ),
    path(
        "<int:movie_id>/favorite/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),
    path(
        "<int:movie_id>/watched/",
        views.toggle_watched,
        name="toggle_watched",
    ),
]