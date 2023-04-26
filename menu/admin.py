from django.contrib import admin
from .models import Category, Product, Vw_product, Subscription, Order, Invoice
# from django.contrib.auth.admin import UserAdmin

# Register your models here.
from django.contrib import admin

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display        = ('category_name', 'vendor', 'updated_at')
    search_fields       = ('category_name', 'vendor__vendor_name')


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display        = ('product_name', 'vendor', 'price', 'is_available', 'updated_at')
    search_fields       = ('product_name', 'category__name', 'vendor__vendor_name', 'price')
    list_filter         =    ('is_available', 'vendor__vendor_name')
    
    
class Vw_productAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display        = ('product_name', 'category', 'price', 'is_available', 'updated_at')
    search_fields       = ('product_name',)
    list_filter         = ('is_available', 'category')
    
    
class SubscriptionAdmin(admin.ModelAdmin):
    list_display        = ('user', 'product', 'start_date', 'end_date', 'is_active')
    search_fields       = ('user', 'product', 'category')
 
    
class OrderAdmin(admin.ModelAdmin):
    list_display        = ('user', 'product', 'quantity', 'order_date', 'status', 'invoice')
    search_fields       = ('user', 'product', 'order_date', 'status', 'invoice')
    list_filter         = ('user', 'product', 'order_date', 'status')
    
    
class InvoiceAdmin(admin.ModelAdmin):
    list_display        = ('user', 'order', 'product', 'amount', 'paid', 'payment_date')
    search_fields       = ('user', 'order', 'product', 'paid', 'payment_date')
    list_filter         = ('order', 'product', 'paid', 'payment_date')

    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Vw_product, Vw_productAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Invoice, InvoiceAdmin)
