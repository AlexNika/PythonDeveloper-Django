import random

from faker import Faker
from faker.providers import BaseProvider
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, Product
from user_app.models import CoreUser
from .constants import TEST_IMAGE_PATH


class CategoryShortName(BaseProvider):

    @classmethod
    def cshn_generate(cls):
        category_short_name = ['CBI', 'CFS', 'CCI', 'REF', 'RFW', 'DWS', 'WMS', 'HOB', 'HOO', 'TGC', 'MWS']
        return random.choice(category_short_name)


class ProductTestCase(TestCase):

    def setUp(self):
        Faker.seed(42)
        faker = Faker('ru_RU')
        faker.add_provider(CategoryShortName)
        user = CoreUser.objects.create_user(username=faker.name(), email=faker.email(), is_manager=faker.boolean())
        category = Category.objects.create(category_short_name=faker.cshn_generate(),
                                           category_name=faker.words(),
                                           user=user)

        self.product = Product.objects.create(product_code='42',
                                              product_index=42,
                                              product_eancode='42',
                                              product_category=category,
                                              user=user)

    def test_full_code(self):
        self.assertEqual(self.product.get_full_code(), '42.42.42')

    def test_get_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), '/product_detail/42/')


class CategoryTestCase(TestCase):
    def test_has_image(self):
        Faker.seed(42)
        faker = Faker('ru_RU')
        faker.add_provider(CategoryShortName)
        user = CoreUser.objects.create_user(username=faker.name(), email=faker.email(), is_manager=faker.boolean())
        category = Category()
        category.category_short_name = faker.cshn_generate()
        category.category_name = faker.words()
        category.category_description = faker.text()
        category.user = user
        category.category_image = SimpleUploadedFile(name='test_image.jpg', content=open(TEST_IMAGE_PATH, 'rb').read())
        category.save()
        self.assertTrue(category.has_image())
