from django.urls import path

from . import views


app_name = "games"

urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),
    path(
        "admin/",
        views.admin,
        name="admin",
    ),
    path(
        "admin/create/",
        views.create,
        name="create",
    ),
    path(
        "admin/<int:game_id>/edit/",
        views.edit,
        name="edit",
    ),
    path(
        "<int:game_id>/rate/",
        views.rate,
        name="rate",
    ),
    path(
        "rating/<int:rating_id>/delete/",
        views.delete_rating,
        name="delete_rating",
    ),
    path(
        "admin/<int:game_id>/delete/",
        views.delete,
        name="delete",
    ),
    path(
        "screenscraper/search/",
        views.screenscraper_search,
        name="screenscraper_search",
    ),
    path(
        "<int:game_id>/",
        views.detail,
        name="detail",
    ),
]