from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),
    path('save_vendor/<slug:vendor_slug>/', views.save_vendor, name='save_vendor'),
    path('send_message_to_vendor/<slug:vendor_slug>/', views.send_message_to_vendor, name='send_message_to_vendor'),
    
    # ADD TO CART
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # DECREASE TO CART
    path('decrease_cart/<int:product_id>/', views.decrease_cart, name='decrease_cart'),
    # DELTE CART ITEM
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart')
]
