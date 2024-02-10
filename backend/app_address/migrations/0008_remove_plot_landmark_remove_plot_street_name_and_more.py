# Generated by Django 5.0 on 2023-12-28 02:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_address', '0007_alter_locality_sub_locality_name_landmark_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plot',
            name='landmark',
        ),
        migrations.RemoveField(
            model_name='plot',
            name='street_name',
        ),
        migrations.CreateModel(
            name='LandmarkPlotRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp_id', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('active_status', models.BooleanField(default=True)),
                ('custom_id', models.CharField(editable=False, max_length=255, unique=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('landmark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landmark_plot_relationships', to='app_address.landmark')),
                ('plot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landmark_plot_relationships', to='app_address.plot')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StreetPlotRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp_id', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('active_status', models.BooleanField(default=True)),
                ('custom_id', models.CharField(editable=False, max_length=255, unique=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('plot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='street_plot_relationships', to='app_address.plot')),
                ('street', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='street_plot_relationships', to='app_address.street')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]