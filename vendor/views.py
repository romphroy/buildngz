from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Vendor
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_vendor

# from .forms import UserForm

# from django.contrib import messages

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