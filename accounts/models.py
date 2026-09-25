from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    avatar = models.ImageField(upload_to="avatars/", blank=True)
    bio = models.TextField(blank=True)