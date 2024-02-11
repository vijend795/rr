# Generated by Django 5.0 on 2024-02-10 21:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_address', '0011_locality_district_locality_tehsil'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DynamicRelationAreaLocality',
            new_name='AreaLocalityRelationship',
        ),
        migrations.AlterUniqueTogether(
            name='landmark',
            unique_together={('name', 'area')},
        ),
        migrations.AlterUniqueTogether(
            name='street',
            unique_together={('name', 'area')},
        ),
    ]