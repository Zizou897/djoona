from django.contrib import admin
from django.urls import path
from djona_admin import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.IndexPage,name='index'),  
    path('produit', views.Produit, name='product'),
    path('product/<str:id>/', views.ProductDetailPage, name='product_detail'),
    path('recherche-vehicule/', views.searchCar, name='recherche'),
    path("achat", views.AchatPage, name="achat"),
    path("slide", views.common_view, name="slide"),
    path("carrosseriePlus", views.carrosseriePage, name="carrosseriePlus"),
    
    path('contact/', views.ContactConsPage, name='contactCons'),
    path('contactVehi/<int:product_id>/', views.ContactPage, name='contact'),
    

    # path("product/vendre", views.ProductBuyPage, name="productbuy"),
    path("about", views.AboutPage, name="about"),
    path("rejoindre", views.RejoindrePage, name="rejoindre"),
    path("location", views.LocationPage, name="location"),
    path('piece-detache', views.piece_detache, name='piece-detache'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
