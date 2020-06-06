from django.test import Client
from django.test import TestCase
from faker import Faker
from mixer.backend.django import mixer

from .models import Category, Product
from user_app.models import CoreUser
from .tests import CategoryShortName


class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        Faker.seed(42)
        faker = Faker('ru_RU')
        faker.add_provider(CategoryShortName)
        self.name = faker.name()
        self.email = faker.email()
        self.message = faker.text()
        self.user = CoreUser.objects.create_user(username=faker.name(), email=faker.email(),
                                                 is_manager=faker.boolean())
        self.category = mixer.blend(Category, user=self.user)
        self.product = mixer.blend(Product, user=self.user)

    def test_get_status200(self):
        # 'get' for /
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # 'get' for /feedback/
        response = self.client.get('/feedback/')
        self.assertEqual(response.status_code, 200)

        # 'get' for /categories/
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)

        # 'get' for category get_absolute_url() method
        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        # 'get' for product get_absolute_url() method
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_get_status404(self):
        # 'get' for /abracadabra/
        response = self.client.get('/abracadabra/')
        self.assertEqual(response.status_code, 404)

    def test_post_status302(self):
        # post method to /feedback/
        response = self.client.post('/feedback/', {'name': self.name, 'email': self.email, 'message': self.message})
        self.assertEqual(response.status_code, 302)

        # post method to /category_create/
        response = self.client.post('/category_create/', {'category_short_name': self.category.category_short_name,
                                                          'category_name': self.category.category_name,
                                                          'user': self.user})
        self.assertEqual(response.status_code, 302)

    def test_context(self):
        response = self.client.get('/categories/')
        self.assertTrue('category_list' in response.context)

    def test1_login_required(self):
        CoreUser.objects.create_user(username='test1_user', email='test1@test1.com',
                                     is_active=True, password='qwerty123456')
        response = self.client.get('/category_create/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='test1_user', password='qwerty123456')
        response = self.client.get('/category_create/')
        self.assertEqual(response.status_code, 200)

    def test2_login_required(self):
        CoreUser.objects.create_user(username='test_user2', email='test2@test2.com',
                                     is_active=True, is_superuser=True,
                                     password='123456qwerty')

        response = self.client.get('/registration/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='test_user2', password='123456qwerty')
        response = self.client.get('/registration/')
        self.assertEqual(response.status_code, 200)
