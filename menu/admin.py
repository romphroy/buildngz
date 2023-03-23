from django.contrib import admin
from .models import Category, Product
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
    
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
