import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


def get_user_auth():
    user_config = {'user_login': os.getenv('HANSA_LOGIN'),
                   'user_password': os.getenv('HANSA_PASSWORD')}
    return user_config


class CoreUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_manager = models.BooleanField(default=False)

    class Meta:
        ordering = ["username"]

    def get_absolute_url(self):
        return reverse("user_app:user_detail", kwargs={"slug": self.id})
