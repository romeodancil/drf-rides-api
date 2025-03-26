# Generated by Django 4.2.20 on 2025-03-26 03:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manageRide', '0003_ridemodel_rideeventmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ridemodel',
            name='id_driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rides_as_driver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ridemodel',
            name='id_rider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rides_as_rider', to=settings.AUTH_USER_MODEL),
        ),
    ]
