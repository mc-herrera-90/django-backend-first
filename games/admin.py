from django.contrib import admin

from .models import Game, Platform


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "identifier",
        "icon",
    )

    search_fields = (
        "name",
        "identifier",
    )


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "platform",
        "year",
        "genre",
        "developer",
        "user",
    )

    search_fields = (
        "title",
        "genre",
        "developer",
        "publisher",
    )

    list_filter = (
        "platform",
        "year",
        "genre",
    )

    list_select_related = (
        "platform",
        "user",
    )
