from django.db import models
from ckeditor.fields import RichTextField
# from django.db.models.fields.related import ForeignKey, OneToOneField

from accounts.models import User, UserProfile
from accounts.utils import send_notification
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    insurance_cert = models.ImageField(upload_to='vendor/insurance_cert')
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.CharField(max_length=9, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True)
    years_in_business = models.IntegerField(blank=True, null=True)
    minimum_project_size = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    maximum_project_size = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    specialties = models.TextField(blank=True)
    service_area = models.CharField(max_length=255, blank=True)
    languages_spoken = models.TextField(blank=True)
    accepted_payment_methods = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    awards = models.TextField(blank=True)
    insurance_carrier = models.CharField(max_length=255, blank=True)
    policy_number = models.CharField(max_length=255, blank=True)
    hours_of_operation = models.JSONField(blank=True, null=True)
    business_categories = models.CharField(max_length=255, blank=True)
    is_approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.vendor_name
    
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/email/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                }
                if self.is_approved == True:
                    # Send notification email
                    mail_subject = 'Buildngz Pro account approved.'
                    send_notification(mail_subject, mail_template, context)
                else:
                    # Send notification email
                    mail_subject = "Buildngz Pro account approval rejected"
                    send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args,  **kwargs)
    
    
# Create your models here.
# class Conversation(models.Model):
#     participants = models.ManyToManyField(User, related_name='conversations')

    
class Message(models.Model):
    vendor      = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    sender_name = models.CharField(max_length=100)
    sender_email= models.EmailField()
    recipients  = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='received_messages')
    subject     = models.CharField(max_length=255)
    body        = RichTextField(blank=True, null=True)
    sent_at     = models.DateTimeField(auto_now_add=True)
    parent      = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    read        = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('message_detail', args=[str(self.id)])


# class Inbox(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inbox')
#     messages = models.ManyToManyField(Message, related_name='inboxes')

#     def __str__(self):
#         return f"Inbox for {self.user.username}"
    
    
# class Attachment(models.Model):
#     message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
#     file = models.FileField(upload_to='attachments/')

# class Notification(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
#     message = models.ForeignKey(Message, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     read = models.BooleanField(default=False)
    
    

    