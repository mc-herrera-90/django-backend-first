from django.contrib import admin

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "year",
        "genre",
        "director",
        "studio",
    )

    list_filter = (
        "genre",
        "year",
        "country",
    )

    search_fields = (
        "title",
        "director",
        "studio",
    )