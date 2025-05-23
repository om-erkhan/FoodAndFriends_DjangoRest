# Generated by Django 5.1.2 on 2025-05-13 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantsModule', '0011_restaurant_preferences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='ambience',
            field=models.CharField(choices=[('CASUAL', 'Casual'), ('FAMILY', 'Family'), ('OUTDOOR', 'Outdoor'), ('ROMANTIC', 'Romantic')], default='CASUAL', max_length=20),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='delivery',
            field=models.CharField(choices=[('NONE', 'None'), ('IN_HOUSE', 'In House')], default='NONE', max_length=20),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='preferences',
            field=models.CharField(choices=[('JAPENESE', 'Japenese'), ('CHINESE', 'Chinese'), ('DESI', 'Desi')], default='JAPENESE', max_length=20),
        ),
    ]
