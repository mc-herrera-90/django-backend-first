from django.conf import settings
from django.db import models

class Platform(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    identifier = models.CharField(
        max_length=50,
        unique=True,
    )

    icon = models.ImageField(
        upload_to="platforms/",
        blank=True,
    )

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    developer = models.CharField(max_length=150)

    platform = models.ForeignKey(
        Platform,
        on_delete=models.PROTECT,
        related_name="games",
    )

    publisher = models.CharField(max_length=150)

    portrait = models.ImageField(
        upload_to="games/portraits/",
        blank=True,
    )

    cartridge = models.ImageField(
        upload_to="games/cartridges/",
        blank=True,
    )

    marquee = models.ImageField(
        upload_to="games/marquees/",
        blank=True,
    )

    video = models.FileField(
        upload_to="games/videos/",
        blank=True,
    )

    technical_sheet = models.FileField(
        upload_to="games/technical_sheets/",
        blank=True,
    )

    description = models.TextField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="games",
    )

    def save(self, *args, **kwargs):

        if self.pk:

            old_game = Game.objects.get(pk=self.pk)

            file_fields = (
                "portrait",
                "marquee",
                "video",
                "technical_sheet",
            )

            for field_name in file_fields:

                old_file = getattr(old_game, field_name)
                new_file = getattr(self, field_name)

                if old_file and old_file != new_file:
                    old_file.delete(save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class GameRating(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="ratings",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="game_ratings",
    )

    rating = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["game", "user"],
                name="unique_game_rating_per_user",
            ),
        ]
