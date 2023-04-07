from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify
from django.db.models import Count

from .models import Vendor, Message
        
from .forms import VendorForm, NewVendorMessageForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_vendor
from menu.models import Category, Product
from menu.forms import CategoryForm, ProductForm

# from django.contrib import messages


# Helper Function
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorProfile(request):
    print('I am in the right routine') 
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    
    if request.method == 'POST':
        print(request.POST) 
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            print('I made into the save block') 
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Your business profile has been updated.')
            return redirect('vendorProfile')
        else:
            if profile_form.errors != '':
                error_message = profile_form.errors
            elif vendor_form.errors != '':
                error_message = vendor_form.errors
            # messages.error(request, error_message)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vendorProfile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorInbox(request):
    vendor  = get_vendor(request)
    messages= Message.objects.filter(vendor=vendor).order_by('sent_at')
    message_count= messages.count()
    context = {
        'messages': messages,
        'message_count': message_count,
     }
    return render(request, 'vendor/vendorInbox.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def readMessage(request, pk=None):
    vendor  = get_vendor(request)
    messages= Message.objects.filter(vendor=vendor).order_by('sent_at')
    message = get_object_or_404(Message, pk=pk)
    message_count= messages.count()
    context = {
        'message': message,
        'message_count': message_count,
     }
    return render(request, 'vendor/readMessage.html', context)



def composeMessage(request):
    vendor = get_vendor(request)
    
    print(vendor)
    if request.method == 'POST':
        print(request.POST)
        form = NewVendorMessageForm(request.POST)
        if form.is_valid():
            print(request.POST)       
            recipients          = form.cleaned_data['recipients']
            subject             = form.cleaned_data['subject']
            body                = form.cleaned_data['body']
            message             = form.save(commit=False)
            message.sender_name = vendor.user.first_name + ' ' + vendor.user.last_name
            message.sender_email= vendor.user.email
            
            form.save()
            message.recipients.set(recipients)
            return redirect('vendorInbox', request)
        else:
            form = NewVendorMessageForm()
            messages= Message.objects.filter(vendor=vendor).order_by('sent_at')
            message_count= messages.count()
                    
            context = {
                'vendor': vendor,
                'form': form,
                'message_count': message_count,
            }
            return render(request, 'vendor/composeMessage.html', context)

def vendorCalendar(request):
    return render(request, 'vendor/vendorCalendar.html')


def vendorListings(request):
    return render(request, 'vendor/vendorListings.html')


def customers(request):
    return render(request, 'vendor/customers.html')


def vendors(request):
    return render(request, 'vendor/vendors.html')


def incomeTracker(request):
    return render(request, 'vendor/incomeTracker.html')


def billTracker(request):
    return render(request, 'vendor/billTracker.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menuBuilder(request):
    vendor          = get_vendor(request)
    categories      = Category.objects.filter(vendor=vendor).order_by('category_name').annotate(num_products=Count('products'))
    context     = {
        'categories': categories,
     }
    return render(request, 'vendor/menuBuilder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def product_by_category(request, pk=None):
    vendor          = get_vendor(request)
    category        = get_object_or_404(Category, pk=pk)
    product         = Product.objects.filter(vendor=vendor, category=category).order_by('product_name')
    context     = {
        'product': product,
        'category': category,
    }
    return render(request, 'vendor/product_by_category.html', context)
    
    
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def addCategory(request):
    if request.method == 'POST':
        print(request.POST)
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name   = form.cleaned_data['category_name']
            category        = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug   = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('menuBuilder')
        else:
            error_message = form.errors
            messages.error(request, error_message)

    else:
        form = CategoryForm()
    context = {
        'form': form
    }
    return render(request, 'vendor/addCategory.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def editCategory(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        print(request.POST)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name   = form.cleaned_data['category_name']
            category        = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug   = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('menuBuilder')
        else:
            error_message = form.errors
            messages.error(request, error_message)

    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/editCategory.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def deleteCategory(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has be deleted successfully.')
    return redirect('menuBuilder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def addProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            product_name   = form.cleaned_data['product_name']
            product        = form.save(commit=False)
            product.vendor = get_vendor(request)
            product.slug   = slugify(product_name)
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('product_by_category', product.category.id)
        else:
            print(form.errors)
            # messages.error(request, error_message)
    else:
        form = ProductForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form
    }
    return render(request, 'vendor/addProduct.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def editProduct(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        print(request.POST)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product_name   = form.cleaned_data['product_name']
            product        = form.save(commit=False)
            product.vendor = get_vendor(request)
            product.slug   = slugify(product_name)
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_by_category', product.category.id)
        else:
            error_message = form.errors
            messages.error(request, error_message)

    else:
        form = ProductForm(instance=product)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'vendor/editProduct.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def deleteProduct(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product has be deleted successfully.')
    return redirect('product_by_category', product.category.id)    