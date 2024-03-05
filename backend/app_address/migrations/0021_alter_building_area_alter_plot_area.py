# Generated by Django 5.0 on 2024-03-04 08:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_address', '0020_alter_tower_options_building_area_alter_floor_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='area',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='building', to='app_address.area', verbose_name='area'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='plot',
            name='area',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='plot', to='app_address.area', verbose_name='area'),
            preserve_default=False,
        ),
    ]