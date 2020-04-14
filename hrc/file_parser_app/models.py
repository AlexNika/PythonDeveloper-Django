from django.db import models


class File(models.Model):
    file_name = models.FileField(upload_to='uploads/')
    file_description = models.CharField(max_length=256, blank=True, null=True)
    file_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.file_name)
