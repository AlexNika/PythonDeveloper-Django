from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from core_app.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Заполенние мадели Category
        try:
            Category.objects.create(category_short_name='CBI', category_name='Духовые шкафы')
            Category.objects.create(category_short_name='HOB', category_name='Варочные поверхности')
            Category.objects.create(category_short_name='CFS', category_name='Отдельностоящие плиты')
            Category.objects.create(category_short_name='MWS', category_name='Микроволновые печи')
            Category.objects.create(category_short_name='REF', category_name='Холодильники')
            Category.objects.create(category_short_name='DWS', category_name='Посудомоечные машины')
            Category.objects.create(category_short_name='WMS', category_name='Стиральные машины')
            Category.objects.create(category_short_name='HOOD', category_name='Вытяжки')
            Category.objects.create(category_short_name='RWS', category_name='Винные шкафы')
        except IntegrityError:
            print(f'Модель Category уже заполнена')
