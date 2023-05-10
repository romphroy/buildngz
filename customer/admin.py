from django.contrib import admin
from .models import SavedVendor

# Register your models here.
class SavedVendorAdmin(admin.ModelAdmin):
    list_display        = ('user', 'vendor', 'created_at')

admin.site.register(SavedVendor)
