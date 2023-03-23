from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify

from .models import Vendor
from .forms import VendorForm
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
        print('I made into the post check if') 
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


def vendorInbox(request):
    return render(request, 'vendor/vendorInbox.html')


def vendorCalendar(request):
    return render(request, 'vendor/vendorCalendar.html')


def vendorListings(request):
    return render(request, 'vendor/vendorListings.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menuBuilder(request):
    vendor      = get_vendor(request)
    categories  = Category.objects.filter(vendor=vendor).order_by('category_name')
    context     = {
        'categories': categories,
    }
    return render(request, 'vendor/menuBuilder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def product_by_category(request, pk=None):
    vendor      = get_vendor(request)
    category    = get_object_or_404(Category, pk=pk)
    product     = Product.objects.filter(vendor=vendor, category=category)
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
        print(request.POST)
        form = ProductForm(request.POST)
        if form.is_valid():
            product_name   = form.cleaned_data['product_name']
            product        = form.save(commit=False)
            product.vendor = get_vendor(request)
            product.slug   = slugify(product_name)
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('menuBuilder')
        else:
            error_message = form.errors
            messages.error(request, error_message)

    else:
        form = ProductForm()
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
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product_name   = form.cleaned_data['product_name']
            product        = form.save(commit=False)
            product.vendor = get_vendor(request)
            product.slug   = slugify(product_name)
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('menuBuilder')
        else:
            error_message = form.errors
            messages.error(request, error_message)

    else:
        form = ProductForm(instance=product)
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
    return redirect('menuBuilder')    