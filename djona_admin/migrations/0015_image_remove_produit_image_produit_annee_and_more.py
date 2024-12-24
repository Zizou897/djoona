# Generated by Django 5.1.3 on 2024-12-14 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djona_admin', '0014_remove_produit_annee_remove_produit_etat_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.RemoveField(
            model_name='produit',
            name='image',
        ),
        migrations.AddField(
            model_name='produit',
            name='annee',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produit',
            name='neuf_ou_occasions',
            field=models.CharField(choices=[('neuf', 'Neuf'), ('occasion', 'Occasion')], default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produit',
            name='ville',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produit',
            name='images',
            field=models.ManyToManyField(related_name='produits', to='djona_admin.image'),
        ),
    ]
