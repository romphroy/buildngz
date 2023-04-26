from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),
    path('send_message_to_vendor/<slug:vendor_slug>/', views.send_message_to_vendor, name='send_message_to_vendor'),
    
    # ADD TO CART
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
