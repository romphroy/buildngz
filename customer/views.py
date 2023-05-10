from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied 
from django.template.defaultfilters import slugify

from accounts.forms import UserForm
from accounts.models import User, UserProfile
from accounts.utils import detectUser, send_verification_email
from accounts.views import check_role_customer
from menu.models import Vw_product
from marketplace.models import Cart
from .models import SavedVendor


# Helper Function
def get_customer(request):
    customer = User.objects.get(user=request.user)
    return customer


def c_profile(request):
    return render(request, 'customer/c_profile.html')


# @login_required(login_url='login')
# @user_passes_test(check_role_customer)
# def c_my_account(request):
#     print('I am in the right routine') 
#     profile = get_object_or_404(UserProfile, user=request.user)
#     customer= get_object_or_404(User, id=request.user.id)
#     category= get_object_or_404(Vw_category, pk=pk)
#     product = Vw_product.objects.filter(customer=customer, category__name='Customer').order_by('product_name')

#     context = {
#         'profile': profile,
#         'customer': customer,
#         'category': category,
#         'product': product
#     }
#     return render(request, 'customer/my_account.html', context)

# @login_required(login_url='login')
# @user_passes_test(check_role_customer)
# def c_my_account(request):
#     profile = get_object_or_404(UserProfile, user=request.user)
#     customer= get_object_or_404(User, id=request.user.id)
#     products = Vw_product.objects.filter(vw_category__category_name='Buyer').order_by('product_name')

#     context = {
#         'profile': profile,
#         'customer': customer,
#         'products': products
#     }
#     return render(request, 'customer/my_account.html', context)

    category    = get_object_or_404(Vw_category, pk=pk)
    product     = Product.objects.filter(vendor=vendor, category__name='Vendor').order_by('product_name')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def c_my_account(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    customer = get_object_or_404(User, id=request.user.id)
    products = Vw_product.objects.filter(category='Buyer').order_by('product_name')
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = 0

    context = {
        'profile': profile,
        'customer': customer,
        'products': products,
        'cart_items': cart_items,
    }
    return render(request, 'customer/my_account.html', context)


def c_bookings(request):
    return render(request, 'customer/c_bookings.html')


def c_rfps(request):
    return render(request, 'customer/c_rfps.html')


def c_reviews(request):
    return render(request, 'customer/c_reviews.html')


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def c_bookmarks(request):
    saved_vendors = SavedVendor.objects.filter(user=request.user).select_related('vendor')
    print(saved_vendors)
    context = {
        'saved_vendors': saved_vendors,
    }
    return render(request, 'customer/c_bookmarks.html', context)


def c_messages(request):
    # return render(request, 'customer/c_messages.html')
    return render(request, 'marketplace/cart-2.html')


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def product_by_category(request, pk=None):
    customer    = get_customer(request)
    product     = Vw_product.objects.filter(customer=customer, category_name='Buyer').order_by('product_name')
    context     = {
        'product': product,
    }
    return render(request, 'vendor/product_by_category.html', context)
    
    
