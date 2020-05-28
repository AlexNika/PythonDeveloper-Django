from django.db import models
from user_app.models import CoreUser


class TimeStamp(models.Model):
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class File(TimeStamp):
    file_name = models.FileField(upload_to='uploads/')
    file_description = models.CharField(max_length=256, blank=True, null=True)
    user = models.ForeignKey(CoreUser, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return str(self.file_name)

    def has_file(self):
        return bool(self.file_name)
