# Generated by Django 5.2.3 on 2025-06-23 15:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApis', '0002_createprofilemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpverification',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
