# Generated by Django 5.1.3 on 2024-12-14 08:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djona_admin', '0019_produit_annee_produit_occasion_neuve'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('date_ajout', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='produit',
            name='image',
        ),
        migrations.AlterField(
            model_name='produit',
            name='annee',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='produit',
            name='carburant',
            field=models.CharField(choices=[('essence', 'Essence'), ('diesel', 'Diesel'), ('hybride', 'Hybride'), ('electrique', 'Électrique')], max_length=50),
        ),
        migrations.AlterField(
            model_name='produit',
            name='kilometrage',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='produit',
            name='occasion_neuve',
            field=models.CharField(help_text="Indiquez si le véhicule est neuf ou d'occasion.", max_length=255),
        ),
        migrations.AlterField(
            model_name='produit',
            name='prix',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='produit',
            name='prix_location',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='produit',
            name='transmission',
            field=models.CharField(choices=[('manuelle', 'Manuelle'), ('automatique', 'Automatique')], max_length=50),
        ),
        migrations.AddField(
            model_name='produit',
            name='images',
            field=models.ManyToManyField(related_name='produits', to='djona_admin.image'),
        ),
    ]
