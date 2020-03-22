# Generated by Django 3.0.4 on 2020-03-21 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.FileField(upload_to='uploads/')),
                ('file_description', models.CharField(blank=True, max_length=256, null=True)),
                ('file_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]