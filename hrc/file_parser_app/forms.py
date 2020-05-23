import os
from django import forms

from core_app.constants import BASE_GOODS_FILE_NAME, BASE_PRICE_FILE_NAME, BASE_MRKTD_FILE_NAME, true_ext
from .models import File


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ['user']

    @staticmethod
    def get_filename(file_name):
        return os.path.splitext(str(file_name))[0]

    @staticmethod
    def get_ext(file_name):
        return os.path.splitext(str(file_name))[1]

    def is_valid(self):
        super(FileForm, self).is_valid()
        file_name = self.cleaned_data['file_name']
        ext = FileForm.get_ext(file_name)
        fn = FileForm.get_filename(file_name)
        if BASE_GOODS_FILE_NAME not in fn or BASE_PRICE_FILE_NAME not in fn or BASE_MRKTD_FILE_NAME not in fn:
            if ext not in true_ext:
                return False
        return True

