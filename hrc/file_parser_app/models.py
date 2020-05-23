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
    su_pk = CoreUser.objects.filter(is_superuser=True)[0]
    user = models.ForeignKey(CoreUser, default=su_pk.pk, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.file_name)

    def has_file(self):
        return bool(self.file_name)
