# Generated by Django 3.0.7 on 2020-06-26 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0009_auto_20200626_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_internal_path',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]