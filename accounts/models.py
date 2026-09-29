from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
    )

    bio = models.TextField(
        blank=True,
    )

    def save(self, *args, **kwargs):
        old_avatar = None

        if self.pk:
            try:
                old_user = type(self).objects.get(pk=self.pk)
                old_avatar = old_user.avatar
            except type(self).DoesNotExist:
                pass

        super().save(*args, **kwargs)

        if (
            old_avatar
            and old_avatar.name
            and old_avatar.name != self.avatar.name
        ):
            if default_storage.exists(old_avatar.name):
                default_storage.delete(old_avatar.name)

    def delete(self, *args, **kwargs):
        avatar_name = self.avatar.name if self.avatar else None

        super().delete(*args, **kwargs)

        if avatar_name and default_storage.exists(avatar_name):
            default_storage.delete(avatar_name)