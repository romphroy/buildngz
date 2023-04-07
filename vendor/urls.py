from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
        path('', AccountViews.vendorDashboard, name='vendor'),
        path('vendorProfile/', views.vendorProfile, name='vendorProfile'),
        path('vendorInbox/', views.vendorInbox, name='vendorInbox'),
        path('vendorInbox/message/<int:pk>/', views.readMessage, name='readMessage'),
        path('vendorInbox/message/compose/', views.composeMessage, name='composeMessage'),

        path('vendorCalendar/', views.vendorCalendar, name='vendorCalendar'),
        path('vendorListings/', views.vendorListings, name='vendorListings'),
        path('menuBuilder/', views.menuBuilder, name='menuBuilder'),
        path('menuBuilder/category/<int:pk>/', views.product_by_category, name='product_by_category'),
        
        # Category CRUD
        path('menuBuilder/category/add/', views.addCategory, name='addCategory'),
        path('menuBuilder/category/edit/<int:pk>/', views.editCategory, name='editCategory'),
        path('menuBuilder/category/delete/<int:pk>/', views.deleteCategory, name='deleteCategory'),
        
        # Product CRUD
        path('menuBuilder/product/add/', views.addProduct, name='addProduct'),
        path('menuBuilder/product/edit/<int:pk>/', views.editProduct, name='editProduct'),
        path('menuBuilder/product/delete/<int:pk>/', views.deleteProduct, name='deleteProduct'),
        
        # Quickbook Look alike screens
        path('incomeTracker/', views.incomeTracker, name='incomeTracker'),
        path('billTracker/', views.billTracker, name='billTracker'),
        path('customers/', views.customers, name='customers'),
        path('vendors/', views.vendors, name='vendors'),
        
    ]
