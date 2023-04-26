from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.customerDashboard, name='customer'),
    path('c_profile/', views.c_profile, name='c_profile'),
    path('c_my_account/', views.c_my_account, name='c_my_account'),

    path('c_bookings/', views.c_bookings, name='c_bookings'),
    path('c_rfps/', views.c_rfps, name='c_rfps'),
    path('c_reviews/', views.c_reviews, name='c_reviews'),
    path('c_bookmarks/', views.c_bookmarks, name='c_bookmarks'),
    path('c_messages/', views.c_messages, name='c_messages'),  
]