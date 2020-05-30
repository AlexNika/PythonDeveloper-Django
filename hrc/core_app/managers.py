from django.db import models


class ActiveManager(models.Manager):

    def get_queryset(self):
        all_objects = super(ActiveManager, self).get_queryset()
        return all_objects.filter(is_active=True)
