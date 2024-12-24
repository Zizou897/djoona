from django.contrib import admin
from django.utils.html import mark_safe
from djona_admin.models import CarouselImage, Image, Produit, EtatVehicule, Reservation, PieceDetache

# Register your models here.
    
class AdminProduit(admin.ModelAdmin):
    list_display = (
        'id', 'first_image', 'marque', 'modele', 'carburant', 'type', 'ville', 'annee', 'nom_entreprise', 'contact', 'date_ajout'
    )
    
    search_fields = ('marque', 'modele', 'ville', 'nom_entreprise', 'contact', 'annee')
    list_filter = ('carburant', 'type', 'ville', 'date_ajout')

    def first_image(self, obj):
        image = obj.images.first()
        if image and hasattr(image, 'image') and image.image:
            return mark_safe(f'<img src="{image.image.url}" width="50" height="50" style="border-radius: 5px;" />')
        return 'Aucune image'

    first_image.short_description = 'Image'

    ordering = ('-date_ajout',)

    

class AdminImage(admin.ModelAdmin):
    list_display = ('image', 'date_ajout')
    
    
class AdminCarouselImage(admin.ModelAdmin):
    list_display = ('image_url',)
    
    
        
class AdminEtatVehicule(admin.ModelAdmin):
    list_display = ('nom', 'date_ajout')
    
    
        
class AdminReservation(admin.ModelAdmin):
    list_display = ('id', 'produit', 'client_nom', 'client_prenom', 'client_email', 'client_telephone', 'date_reservation')


class AdminPieceDetache(admin.ModelAdmin):
    list_display = ('images', 'nom', 'prix_normal', 'prix_reduit', 'date_ajout')
    
    

# Enregistrer les modèles dans l'admin
admin.site.register(Produit, AdminProduit)
admin.site.register(Image, AdminImage)
admin.site.register(CarouselImage, AdminCarouselImage)
admin.site.register(EtatVehicule, AdminEtatVehicule)
admin.site.register(Reservation, AdminReservation)
admin.site.register(PieceDetache, AdminPieceDetache)

