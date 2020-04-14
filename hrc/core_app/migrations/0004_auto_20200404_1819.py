# Generated by Django 3.0.4 on 2020-04-04 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0003_auto_20200404_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(blank=True, choices=[('Z1', 'Active Z1'), ('ZN', 'Active ZN'), ('Z9', 'Active Z9'), ('WS', 'Archive'), ('SZ', 'Sell out')], default='Z9', max_length=2, null=True),
        ),
    ]
