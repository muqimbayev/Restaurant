# Generated by Django 5.0.3 on 2024-03-27 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0003_remove_food_image_food_images_restaurant_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant_location',
            name='latitude',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant_location',
            name='longitude',
            field=models.FloatField(default='1'),
            preserve_default=False,
        ),
    ]
