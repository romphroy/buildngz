from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
        path('', AccountViews.vendorDashboard, name='vendor'),
        path('vendorProfile/', views.vendorProfile, name='vendorProfile'),
        path('vendorInbox/', views.vendorInbox, name='vendorInbox'),
        path('vendorCalendar/', views.vendorCalendar, name='vendorCalendar'),
        path('vendorListings/', views.vendorListings, name='vendorListings'),
    ]
