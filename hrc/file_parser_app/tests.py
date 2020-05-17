from mixer.backend.django import mixer
from django.test import TestCase
from .models import File, CoreUser


class FileUploadTestCase(TestCase):

    def setUp(self):
        user = mixer.blend(CoreUser)
        self.file = mixer.blend(File, user=user)

    def test_upload_file(self):
        self.assertTrue(self.file.has_file())
