from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from vendor.models import Vendor, Message
from menu.models import Category, Product
from django.db.models import Prefetch
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
    return HttpResponse('Testing')