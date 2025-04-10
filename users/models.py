from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", default="default.jpg", blank=True, null=True
    )

    def __str__(self):
        return f"{self.username} ({self.email})"
