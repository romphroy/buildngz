from django.contrib import admin

from .models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'updated_at')
    
# Register your models here.
admin.site.register(Cart, CartAdmin)