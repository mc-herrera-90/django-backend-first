from django.conf import settings
from django.db import models


class Movie(models.Model):
    title = models.CharField(
        max_length=200,
    )

    year = models.PositiveIntegerField()

    genre = models.CharField(
        max_length=100,
    )

    director = models.CharField(
        max_length=150,
    )

    duration = models.PositiveIntegerField(
        help_text="Duración en minutos.",
    )

    country = models.CharField(
        max_length=100,
    )

    language = models.CharField(
        max_length=100,
    )

    studio = models.CharField(
        max_length=150,
    )

    portrait = models.ImageField(
        upload_to="movies/portraits/",
        blank=True,
    )

    landscape = models.ImageField(
        upload_to="movies/landscapes/",
        blank=True,
    )

    trailer = models.FileField(
        upload_to="movies/trailers/",
        blank=True,
    )

    description = models.TextField()

    cast = models.TextField(
        blank=True,
        help_text="Actores principales separados por comas.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    @property
    def cast_list(self):
        return [
            actor.strip()
            for actor in self.cast.split(",")
            if actor.strip()
        ]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-year", "title")


class MovieFavorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorite_movies",
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "movie"],
                name="unique_movie_favorite",
            ),
        ]


class MovieWatched(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watched_movies",
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="watched_by",
    )

    watched_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "movie"],
                name="unique_movie_watched",
            ),
        ]