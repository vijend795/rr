# Generated by Django 5.0 on 2024-02-10 23:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_property', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='address',
        ),
    ]