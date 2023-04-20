from django import forms
from .models import Vendor, Message
from accounts.validators import allow_only_images_validator

class VendorForm(forms.ModelForm):
    insurance_cert = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-default'}), validators=[allow_only_images_validator])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'insurance_cert', 'address', 'country', 'state', 'city', 'zip_code', 'latitude', 'longitude']
        
        
class NewMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('sender_name', 'sender_email', 'subject', 'body')
        labels = {
            'sender_name': 'Name',
            'sender_email': 'Email Address',
            'subject': 'Subject',
            'body': 'Message',
        }
        widgets = {
            'sender_name': forms.TextInput(attrs={'class': 'form-control form-input form-input--large form-input--border-c-gallery'}),
            'sender_email': forms.EmailInput(attrs={'class': 'form-control form-input form-input--large form-input--border-c-gallery'}),
            'subject': forms.TextInput(attrs={'class': 'form-control form-input form-input--large form-input--border-c-gallery'}),
            'body': forms.Textarea(attrs={'class': 'form-control summernote', 'rows': 6}),
        }
        

class NewVendorMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('recipients', 'subject', 'body')
        labels = {
            'recipients': 'To',
            'subject': 'Subject',
            'body': 'Message',
        }
        widgets = {
            'recipients': forms.TextInput(attrs={'class': 'form-control form-input form-input--large form-input--border-c-gallery'}),
            'subject': forms.TextInput(attrs={'class': 'form-control form-input form-input--large form-input--border-c-gallery'}),
            'body': forms.Textarea(attrs={'class': 'form-control form-input form-input--large form-input--border-c-gallery'}),
        }        