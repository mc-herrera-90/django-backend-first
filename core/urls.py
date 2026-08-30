from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "api/wikipedia/person/",
        views.wikipedia_person,
        name="wikipedia_person",
    ),
]