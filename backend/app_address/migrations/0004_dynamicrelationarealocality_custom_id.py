# Generated by Django 5.0 on 2023-12-28 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_address', '0003_dynamicrelationarealocality'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynamicrelationarealocality',
            name='custom_id',
            field=models.CharField(default=1, editable=False, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
