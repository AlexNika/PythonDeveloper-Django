import pandas as pd
from django.db import models


class File(models.Model):
    file_name = models.FileField(upload_to='uploads/')
    file_description = models.CharField(max_length=256, blank=True, null=True)
    file_timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.file_name)

# заготовки...
#     def xls_parse(self):
#         return pd.read_excel(self.file_name)
#
#     def csv_parse(self):
#         return pd.read_csv(self.file_name)
