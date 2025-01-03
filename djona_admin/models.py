import hashlib
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
import time
import uuid
from django.utils.html import mark_safe
from django.core.validators import MinValueValidator



# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name if self.image else "Image sans fichier"
    
    


class CarouselImage(models.Model):
    image_url = models.ImageField(upload_to='carousel_images/')

    def __str__(self):
        return self.image_url.name



    
    
class Produit(models.Model):
    id = models.AutoField(primary_key=True)
    hashed_id = models.CharField(max_length=64, editable=False, unique=True)

    # Relations
    images = models.ManyToManyField('Image', related_name='produits')

    marque = models.CharField(max_length=255)
    modele = models.CharField(max_length=255)
    annee = models.CharField(max_length=4)
    CARBURANT_CHOICES = [
        ('essence', 'Essence'),
        ('diesel', 'Diesel'),
        ('hybride', 'Hybride'),
        ('electrique', 'Électrique'),
    ]
    carburant = models.CharField(max_length=50, choices=CARBURANT_CHOICES)
    type = models.CharField(max_length=255)
    kilometrage = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    TRANSMISSION_CHOICES = [
        ('manuelle', 'Manuelle'),
        ('automatique', 'Automatique'),
    ]
    transmission = models.CharField(max_length=50, choices=TRANSMISSION_CHOICES)
    description = models.TextField()
    ville = models.CharField(max_length=255)
    occasion_neuve = models.CharField(max_length=255, help_text="Indiquez si le véhicule est neuf ou d'occasion.")
    immatriculation = models.CharField(max_length=255, unique=True)
    nom_entreprise = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    
    moteur = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    place = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    couleur_interieur = models.CharField(max_length=255, default='No Color')
    couleur_exterieur = models.CharField(max_length=255, default='No Color')
    cylindre = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    puissance_fiscale = models.PositiveIntegerField(validators=[MinValueValidator(0)])  # Correction ici
    nbre_proprio = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    condition = models.CharField(max_length=255)

    prix_location = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    limite_assurance = models.DateField()
    date_ajout = models.DateTimeField(auto_now=True)

    statut = models.ForeignKey(
        'EtatVehicule',
        on_delete=models.CASCADE,
        related_name='produits'
    )

    # Méthodes
    def first_image_url(self):
        first_image = self.images.first()
        if first_image and hasattr(first_image, 'image') and first_image.image:
            return first_image.image.url
        return None

    first_image_url.short_description = 'Image'

    def image_count(self):
        return self.images.count()
    
    def whatsapp_message(self):
        occasion_neuve = "Neuve" if self.type.lower() == "neuve" else "Occasion"
        image_url = self.first_image_url() if self.first_image_url() else "Image non disponible"
        
        return (
            f"Bonjour, je suis intéressé par le véhicule\n"
            f"Marque: {self.marque}\n" 
            f"Modèle: {self.modele}\n" 
            f"Transmission: {self.transmission}\n"
            f"Prix: {self.prix} FCFA \n"
            f"Kilométrage: {self.kilometrage} km\n"
            f"Année: {self.annee}.\n"
            f"Image du produit: {image_url}\n"
            "Pouvez-vous m'en dire plus ?"
        )
        

    def save(self, *args, **kwargs):
        if not self.hashed_id:
            unique_string = f"{uuid.uuid4()}"
            self.hashed_id = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_ajout']

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.immatriculation})"
    
    


class EtatVehicule(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_ajout']

    def __str__(self):
        return self.nom




class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="reservations")
    client_nom = models.CharField(max_length=255)
    client_prenom = models.CharField(max_length=255)
    client_email = models.EmailField()
    client_telephone = models.CharField(max_length=20)
    adresse = models.CharField(max_length=255)
    date_debut = models.DateField()
    duree = models.PositiveIntegerField()
    date_fin = models.DateField(editable=False)
    date_reservation = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.date_debut:
            self.date_fin = self.date_debut + timedelta(days=self.duree)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Réservation de {self.client_nom} {self.client_prenom} pour {self.produit.marque} {self.produit.modele} du {self.date_debut} au {self.date_fin}"

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-date_reservation'] 
 




class PieceDetache(models.Model):
    id = models.AutoField(primary_key=True)
    images = models.ImageField(upload_to='pieces_detachees/')
    nom = models.CharField(max_length=255, verbose_name="Nom de la pièce")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    prix_normal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix normal")
    prix_reduit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Prix réduit") 
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")

    class Meta:
        ordering = ['-date_ajout']
        verbose_name = "Pièce détachée"
        verbose_name_plural = "Pièces détachées"

    def __str__(self):
        return self.nom