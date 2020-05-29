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

    def save(self, *args, **kwargs):
        super(CoreUser, self).save(*args, **kwargs)
        if not UserProfile.objects.filter(user=self).exists():
            UserProfile.objects.create(user=self)


class UserProfile(models.Model):
    user = models.OneToOneField(CoreUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=256, null=True, blank=True)
    user_role = models.CharField(max_length=256, null=True, blank=True)
    user_photo = models.ImageField(upload_to='users', blank=True, null=True)

    def has_image(self):
        return bool(self.user_photo)
