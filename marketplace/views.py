from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .context_processors import get_cart_amounts, get_cart_counter

from .models import Cart
from customer.models import SavedVendor
from vendor.models import Vendor, Message
from menu.models import Category, Vw_product, Product
from vendor.forms import NewMessageForm


# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True,user__is_active=True).order_by('vendor_name')
    context = {
        'vendors': vendors,
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'products',
            queryset = Product.objects.filter(is_available=True)
        )
    )
    form = NewMessageForm()
    context = {
        'vendor': vendor,
        'categories': categories,
        'form': form,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def send_message_to_vendor(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    
    if request.method == 'POST':
        print(request.POST)
        form = NewMessageForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['sender_name']
            sender_email= form.cleaned_data['sender_email']
            recipients  = [vendor.user]
            subject     = form.cleaned_data['subject']
            body        = form.cleaned_data['body']
            message     = Message(sender_name=sender_name, sender_email=sender_email, subject=subject, body=body)
            message.save()
            message.recipients.set(recipients)
            return redirect('vendor_detail', vendor_slug=vendor.vendor_slug)
        else:
            form = NewMessageForm()
        context = {
            'vendor': vendor,
            'form': form,
        }
        return render(request, 'marketplace/vendor_detail.html', context)
    
def search(request):
    vendor_name = request.GET['vendor_name']
    print(vendor_name)
    return render(request, 'marketplace/listings.html')


def listings(request):
    vendors = Vendor.objects.filter(is_approved=True,user__is_active=True).order_by('vendor_name')
    context = {
        'vendors': vendors,
    }
    return render(request, 'marketplace/listings.html', context)


def add_to_cart(request, product_id=None):
    if request.user.is_authenticated:
        if request.is_ajax():
            # Check if product exists
            try:
                product = Vw_product.objects.get(id=product_id)
                # Check if user has already added it to their cart
                try:
                    chkCart = Cart.objects.get(user=request.user, product=product)
                    # Increase cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, product=product, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Product added to your cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'invalid request'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'This product does not exist'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please sign-in to continue'})
    
    
def decrease_cart(request, product_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            # Check if product exists
            try:
                product = Vw_product.objects.get(id=product_id)
                # Check if user has already added it to their cart
                try:
                    chkCart = Cart.objects.get(user=request.user, product=product)
                    if chkCart.quantity > 1:
                        # Increase cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0                       
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this product in your cart.'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This product does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please sign-in to continue'})


def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items
    }
    return render(request, 'marketplace/cart.html', context)


@login_required(login_url='login')    
def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                # check if cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted.', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart item does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'invalid request'})
            
    return render(request)    


@login_required(login_url='login')    
def save_vendor(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    print(vendor)
    if request.user.is_authenticated:
        saved_vendors = SavedVendor.objects.filter(user=request.user, vendor=vendor)
        if saved_vendors.exists():
            error_message = 'That vendor was already saved.'
            print(error_message)
            message = messages.error(request, error_message)
            context = {
                'vendor': vendor,
                'message': message,
            }
            return render(request, 'marketplace/vendor_detail.html', context)
        else:
            # Save the vendor
            saveVendor = SavedVendor(user=request.user, vendor=vendor)
            saveVendor.save()
            message = messages.success(request, 'Vendor has been saved.')
            context = {
                'vendor': vendor,
                'message': message,
            }
            print('I am validated')
            return render(request, 'marketplace/vendor_detail.html', context)


