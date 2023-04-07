from django.contrib import admin
from vendor.models import Vendor, Message

class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'user', 'created_date', 'is_approved')
    list_displaylinks = ('vendor_name', 'user')
    list_editable = ('is_approved',)
    # ordering = ('vendor_name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'subject', 'sent_at', 'read')
    list_filter = ('sent_at', 'read')
    search_fields = ('sender_name', 'sender_email', 'recipients__username', 'subject', 'body')
    

# Register your models here.
admin.site.register(Vendor, VendorAdmin)