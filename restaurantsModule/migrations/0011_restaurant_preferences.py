# Generated by Django 5.1.2 on 2025-05-13 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantsModule', '0010_restaurant_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='preferences',
            field=models.CharField(choices=[('Japenese', 'japenese'), ('Chinese', 'chinese'), ('Desi', 'desi')], default='Japenese', max_length=20),
        ),
    ]
