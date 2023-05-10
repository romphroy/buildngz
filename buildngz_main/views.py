from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from vendor.models import Vendor
from menu.models import Vw_product

def home(request):
    vendors = Vendor.objects.filter(is_approved=True,user__is_active=True)[:6]
    context = {
        'vendors': vendors,
    }
    return render(request, 'home.html', context)


def pricing(request):
    products = Vw_product.objects.filter(
        Q(product_name__icontains='basic') | 
        Q(product_name__icontains='standard') | 
        Q(product_name__icontains='plus'), 
        is_subscription=True
    ).order_by('price')    
    context = {
        'products': products
    }
    return render(request, 'pricing.html', context)
