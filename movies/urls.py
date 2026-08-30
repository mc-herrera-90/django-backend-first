from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:movie_id>/", views.detail, name="detail"),
]