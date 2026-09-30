from django.contrib import admin

from .models import Game, GameRating, Platform


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


@admin.register(GameRating)
class GameRatingAdmin(admin.ModelAdmin):
    list_display = (
        "game",
        "user",
        "rating",
        "comment",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "game__title",
        "user__username",
    )

    list_filter = (
        "rating",
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "game",
        "user",
    )