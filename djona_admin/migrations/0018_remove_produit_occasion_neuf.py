# Generated by Django 5.1.3 on 2024-12-14 01:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djona_admin', '0017_remove_produit_images_produit_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produit',
            name='occasion_neuf',
        ),
    ]
