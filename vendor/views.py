from django.http.response import HttpResponse
from django.shortcuts import render, redirect

# from .forms import UserForm

# from django.contrib import messages


def vendorProfile(request):
    return render(request, 'vendor/vendorProfile.html')


def vendorInbox(request):
    return render(request, 'vendor/vendorInbox.html')


def vendorCalendar(request):
    return render(request, 'vendor/vendorCalendar.html')


def vendorListings(request):
    return render(request, 'vendor/vendorListings.html')