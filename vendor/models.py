from django.db import models
# from django.db.models.fields.related import ForeignKey, OneToOneField

from accounts.models import User, UserProfile
from accounts.utils import send_notification

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    insurance_cert = models.ImageField(upload_to='vendor/insurance_cert')
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