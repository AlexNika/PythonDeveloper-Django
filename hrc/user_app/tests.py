from faker import Faker
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import CoreUser, UserProfile
from core_app.constants import TEST_IMAGE_PATH


class ProfileCreateTestCase(TestCase):

    def setUp(self):
        Faker.seed(42)
        faker = Faker('ru_RU')
        user = CoreUser.objects.create_user(username=faker.name(), email=faker.email(), is_manager=faker.boolean())
        self.profile = UserProfile.objects.get(user=user)
        self.profile.user_photo = SimpleUploadedFile(name='test_image.jpg', content=open(TEST_IMAGE_PATH, 'rb').read())
        self.profile.save()

    def test_upload_image(self):
        self.assertTrue(self.profile.has_image())
