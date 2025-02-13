# Generated by Django 5.1.3 on 2025-01-03 12:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djona_admin', '0023_piecedetache_alter_carouselimage_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='couleur_exterieur',
            field=models.CharField(default='No Color', max_length=255),
        ),
        migrations.AddField(
            model_name='produit',
            name='couleur_interieur',
            field=models.CharField(default='No Color', max_length=255),
        ),
        migrations.AddField(
            model_name='produit',
            name='cylindre',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produit',
            name='moteur',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produit',
            name='nbre_proprio',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produit',
            name='place',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produit',
            name='puissance_fiscale',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
    ]
