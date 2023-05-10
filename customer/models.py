from django.db import models
from vendor.models import Vendor
from accounts.models import User

# Create your models here.
class SavedVendor(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor      = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='saved_vendor')
    created_at  = models.DateTimeField(auto_now_add=True)