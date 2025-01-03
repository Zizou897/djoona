from glob import escape
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
import hashlib
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from djona_admin.models import CarouselImage, EtatVehicule, Image, PieceDetache, Produit
from django.db.models import Q
from collections import Counter
from collections import defaultdict
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Count, Min



def validate_price_filters(min_price, max_price):
    if min_price and not min_price.isdigit():
        return "Le prix minimum doit être un nombre."
    if max_price and not max_price.isdigit():
        return "Le prix maximum doit être un nombre."
    if min_price.isdigit() and max_price.isdigit() and int(min_price) > int(max_price):
        return "Le prix minimum ne peut pas être supérieur au prix maximum."
    return None

def filter_products(base_queryset, filters):
    return base_queryset.filter(filters) if filters else base_queryset




def IndexPage(request):
    list_products = Produit.objects.all()
    
    whatsapp_message = None
    if list_products.exists():
        whatsapp_message = list_products.first().whatsapp_message()

    vente_statut = EtatVehicule.objects.filter(nom='vente').first()
    location_statut = EtatVehicule.objects.filter(nom='location').first()
    
    all_filtered_products = list_products.filter(
        Q(statut=vente_statut) | Q(statut=location_statut)
    )

    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    selected_type = request.GET.get('type', '').strip().lower()

    error_message = validate_price_filters(min_price, max_price)

    if error_message:
        filters = Q() 
    else:
        filters = Q()
        if min_price.isdigit():
            filters &= Q(prix__gte=int(min_price))
        if max_price.isdigit():
            filters &= Q(prix__lte=int(max_price))
        if selected_type in ["occasion", "neuve"]:
            filters &= Q(type__iexact=selected_type)

    filtered_products = filter_products(all_filtered_products, filters)
    vente_products = filtered_products.filter(statut=vente_statut)
    location_products = filtered_products.filter(statut=location_statut)
    

    if not error_message and not filtered_products.exists():
        error_message = "Aucun véhicule ne correspond aux critères de recherche."

    unique_marques = (
        list_products.values('marque')
        .annotate(product_count=Count('id'))
        .order_by('-product_count')[:6]
    )
    unique_marques_recherche = (
        list_products.values('marque')
        .annotate(product_count=Count('id'))
        .order_by('-product_count')[:6]
    )
    unique_type = (
        list_products.values('type')
        .annotate(product_count=Count('id'))
        .order_by('-product_count')[:6]
    )
    unique_transmission = (
        list_products.values('transmission')
        .annotate(product_count=Count('id'))
        .order_by('-product_count')[:6]
    )
    unique_carburants = (
        list_products.values('carburant')
        .annotate(product_count=Count('id'))
        .order_by('-product_count')[:6]
    )
    selected_marques = [marque['marque'] for marque in unique_marques]
    unique_marques_recherche = [marque['marque'] for marque in unique_marques_recherche]
    # unique_type = [type['type'] for type in unique_type]
    unique_transmission = [transmission['transmission'] for transmission in unique_transmission]
    unique_carburants = [carburant['carburant'] for carburant in unique_carburants]
    

    products_by_marque = {
        marque: list_products.filter(marque=marque)[:4]
        for marque in selected_marques
    }
    products_by_marque_list = [
        (marque, products) for marque, products in products_by_marque.items()
    ]
    vente_marques = (
        vente_products.values_list('marque', flat=True)
        .distinct()
        .order_by('marque')
    )
    location_marques = (
        location_products.values_list('marque', flat=True)
        .distinct()
        .order_by('marque')
    )

    marque_filtered_products = filtered_products.filter(marque__in=selected_marques)

    def get_image_count_and_first_url(product):
        return product.image_count(), product.first_image_url()
    
    type_counts = Counter(product.type.lower() for product in vente_products if product.type)
    
    carrosserie_by_marque = defaultdict(set)
    transmission_by_marque_and_carrosserie = defaultdict(lambda: defaultdict(set))
    
    carburant_by_marque_and_carrosserie_and_transmission = defaultdict(
        lambda: defaultdict(lambda: defaultdict(set))
    )
    
    produits = Produit.objects.all()
    
    for produit in produits:
        carrosserie_by_marque[produit.marque].add(produit.type)
    for produit in produits:
        transmission_by_marque_and_carrosserie[produit.marque][produit.type].add(produit.transmission)
    for produit in produits:
        carburant_by_marque_and_carrosserie_and_transmission[produit.marque][produit.type][produit.transmission].add(produit.carburant)

    carrosserie_by_marque = {marque: list(types) for marque, types in carrosserie_by_marque.items()}
    transmission_by_marque_and_carrosserie = {
        marque: {carrosserie: list(transmissions) for carrosserie, transmissions in carross_dict.items()}
        for marque, carross_dict in transmission_by_marque_and_carrosserie.items()
    }
    carburant_by_marque_and_carrosserie_and_transmission = {
        marque: {
            carrosserie: {
                transmission: list(carburants)
                for transmission, carburants in trans_dict.items()
            }
            for carrosserie, trans_dict in carross_dict.items()
        }
        for marque, carross_dict in carburant_by_marque_and_carrosserie_and_transmission.items()
    }
    

    context = {
        "list_products": marque_filtered_products,
        "products_by_marque": products_by_marque,
        "message": error_message,
        "type_counts": list(type_counts.items()),
        "unique_marques": unique_marques,
        "unique_marques_recherche": unique_marques_recherche,
        # "unique_type": unique_type,
        "unique_transmission": unique_transmission,
        "unique_carburants": unique_carburants,
        "first_image_urls": [get_image_count_and_first_url(product)[1] for product in filtered_products],
        "image_counts": [get_image_count_and_first_url(product)[0] for product in filtered_products],
        "min_price": min_price,
        "max_price": max_price,
        "selected_type": selected_type,
        "whatsapp_message": whatsapp_message,        
        "selected_marques": selected_marques,
        "vente_marques": vente_marques,
        "location_marques": location_marques,
        "products_by_marque_list": products_by_marque_list,
        "carrosserie_by_marque": carrosserie_by_marque,
        "unique_marques": list(carrosserie_by_marque.keys()),
        "transmission_by_marque_and_carrosserie": transmission_by_marque_and_carrosserie,
        "unique_marques": list(transmission_by_marque_and_carrosserie.keys()),
        "carburant_by_marque_and_carrosserie_and_transmission": carburant_by_marque_and_carrosserie_and_transmission,
    }

    return render(request, "index.html", context)




def searchCar(request):
    marque = request.GET.get('marque', '').strip()
    carrosserie = request.GET.get('type', '').strip()
    boite = request.GET.get('transmission', '').strip()
    carburant = request.GET.get('carburant', '').strip()

    error_messages = {
        'marque': None,
        'type': None,
        'transmission': None,
        'carburant': None,
    }

    filtres = Q()
    if marque:
        filtres &= Q(marque__iexact=marque)
        if not Produit.objects.filter(marque__iexact=marque).exists():
            error_messages['marque'] = f"Aucune marque ne correspond à '{marque}'."

    if carrosserie:
        filtres &= Q(type__iexact=carrosserie)
        if not Produit.objects.filter(type__iexact=carrosserie).exists():
            error_messages['type'] = f"Aucun type de carrosserie ne correspond à '{carrosserie}'."

    if boite:
        filtres &= Q(transmission__iexact=boite)
        if not Produit.objects.filter(transmission__iexact=boite).exists():
            error_messages['transmission'] = f"Aucune transmission ne correspond à '{boite}'."

    if carburant:
        filtres &= Q(carburant__iexact=carburant)
        if not Produit.objects.filter(carburant__iexact=carburant).exists():
            error_messages['carburant'] = f"Aucun carburant ne correspond à '{carburant}'."

    produits = Produit.objects.filter(filtres) if filtres else Produit.objects.all()

    message = None
    if not produits.exists():
        message = "Aucun véhicule ne correspond à vos critères."

    paginator = Paginator(produits, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    unique_marques = Produit.objects.values_list('marque', flat=True).distinct()
    unique_carrosseries = Produit.objects.values_list('type', flat=True).distinct()
    unique_boites = Produit.objects.values_list('transmission', flat=True).distinct()
    unique_carburants = Produit.objects.values_list('carburant', flat=True).distinct()

    context = {
        'produits': page_obj.object_list,
        'message': message,
        'error_messages': error_messages, 
        "is_location_page": False,
        "is_piece_detache_page": False, 
        'is_recherche_vehicule_page': True,
        "list_products": page_obj.object_list,
        "page_obj": page_obj,
        "unique_marques": unique_marques,
        "unique_carrosseries": unique_carrosseries,
        "unique_boites": unique_boites,
        "unique_carburants": unique_carburants,
    }

    return render(request, 'recherchevehicule.html', context)




def AchatPage(request):
    list_products = Produit.objects.filter(statut__nom__iexact='vente')
    images = CarouselImage.objects.all()
    
    message = "Aucun véhicule en vente pour l'instant." if not list_products.exists() else ""
    
    paginator = Paginator(list_products, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for product in page_obj.object_list:
        product.hashed_id = hashlib.sha256(str(product.id).encode('utf-8')).hexdigest()

    context = {
        "list_products": page_obj.object_list,
        "message": message,
        "page_obj": page_obj,
        'images': images,
    }
    return render(request, "achat.html", context)




def LocationPage(request):
    list_products = Produit.objects.filter(statut__nom__iexact='location') 
    images = CarouselImage.objects.all()
   
    if list_products.count() < 1:
        message = "Aucun véhicule en location pour l'instant."
    else:
        message = ""

    # Pagination
    paginator = Paginator(list_products, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for product in page_obj.object_list:
        product.hashed_id = hashlib.sha256(str(product.id).encode('utf-8')).hexdigest()

    context = {
        "message": message,
        "page_obj": page_obj,
        "is_location_page": True,
        "is_piece_detache_page": False, 
        'is_recherche_vehicule_page': False,
        'images': images,
    }
    return render(request, "location.html", context)



def piece_detache(request):
    images = PieceDetache.objects.all()    

    if not images.exists():
        message = "Aucune pièce détachée disponible pour le moment."
    else:
        message = None

    context = {
        'message': message, 
    }
    
    return render(request, "piece-detache.html", context)





def ProductDetailPage(request, id):
    product = get_object_or_404(Produit, id=id)
    whatsapp_message = product.whatsapp_message()
    image_urls = [image.image.url for image in product.images.all()]
    images = product.images.all()
    
    statut = product.statut
    
    similar_products = Produit.objects.filter(
        marque=product.marque,
        transmission=product.transmission,
        statut=statut
    ).exclude(id=id) 
    
    similar_products = similar_products[:8]

    context = {
        "product": product,
        "whatsapp_message": whatsapp_message,
        "image_urls": image_urls,
        "images": images,
        'similar_products': similar_products,
        'statut': statut, 
    }
    return render(request, "product_detail.html", context)





def AboutPage(request):
    return render(request, "about.html")



def RejoindrePage(request):
    return render(request, "rejoindre.html")




def ContactConsPage(request):
    return render(request, "contactCons.html")


def carrosseriePage(request):
    type_counts = (
        Produit.objects.values('type')
        .annotate(count=Count('id'))
        .order_by('type')
    )

    first_images = {
        item['type']: Produit.objects.filter(type=item['type'])
        .values_list('images', flat=True)
        .first() or '/static/images/default-car.png'
        for item in type_counts
    }

    context = {
        'type_counts': type_counts,
        'first_images': first_images, 
    }
    return render(request, 'carrosseriePlus.html', context)



def common_view(request):
    images = CarouselImage.objects.all()
    return render(request, 'slide.html', {'images': images})



def ContactPage(request, product_id):
    product = get_object_or_404(Produit, id=product_id)

    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        numero = request.POST.get('numero', '').strip()
        ville = request.POST.get('ville', '').strip()
        email = request.POST.get('email', '').strip()
        description = request.POST.get('description', '').strip()

        if not all([nom, prenom, numero, ville, email, description]):
            messages.error(request, "Tous les champs sont obligatoires.")
            return HttpResponseRedirect(reverse('contact', args=[product.id]))

        subject = f"Demande de contact pour {product.marque} {product.modele}"
        message = (
            f"Nom : {escape(nom)}\n"
            f"Prénom : {escape(prenom)}\n"
            f"Numéro de téléphone : {escape(numero)}\n"
            f"Ville : {escape(ville)}\n"
            f"E-mail : {escape(email)}\n"
            f"Nombre de véhicules : {escape(description)}\n"
        )
        recipient = "contacts@djona.net"

        try:
            send_mail(
                subject,
                message,
                'contacts@djona.net',
                [recipient],
                fail_silently=False,
            )
            messages.success(
                request,
                f"M. {nom}, votre message a bien été envoyé à Djona concernant votre désir de vente de vos {description} véhicule(s).",
            )
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email : {e}")
            messages.error(
                request,
                "Une erreur est survenue lors de l'envoi de votre message. Veuillez réessayer.",
            )

        return redirect('contact', product_id=product.id)

    return render(request, 'contactVehi.html', {'product': product})


