from django.contrib import admin
from vendor.models import Vendor

class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'user', 'created_date', 'is_approved')
    list_displaylinks = ('vendor_name', 'user')
    list_editable = ('is_approved',)
    # ordering = ('vendor_name',)


# Register your models here.
admin.site.register(Vendor, VendorAdmin)