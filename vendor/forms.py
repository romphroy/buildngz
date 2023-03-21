from django import forms
from .models import Vendor
from accounts.validators import allow_only_images_validator

class VendorForm(forms.ModelForm):
    insurance_cert = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-default'}), validators=[allow_only_images_validator])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'insurance_cert']