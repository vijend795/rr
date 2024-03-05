# Generated by Django 5.0 on 2024-02-29 06:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_address', '0018_alter_arealocality_area_alter_arealocality_locality_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='block',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_address.block', verbose_name='block'),
        ),
    ]
