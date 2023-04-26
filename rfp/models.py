# from django.db import models
# from ckeditor.fields import RichTextField
# from django.utils import timezone
# # from django.db.models.fields.related import ForeignKey, OneToOneField

# from accounts.models import User, UserProfile
# from accounts.models import Vendor
# from accounts.utils import send_notification
# from django.conf import settings
# from django.urls import reverse

# # Create your models here.

# class RFP(models.Model):
#     RFP_JOB_TYPE_CHOICES = [
#         ('one-time', 'One-time'),
#         ('ongoing', 'Ongoing'),
#     ]
#     RFP_STATUS_CHOICES = [
#         ('open', 'Open'),
#         ('closed', 'Closed'),
#         ('awarded', 'Awarded'),
#     ]
#     rfp_id = models.AutoField(primary_key=True)
#     customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     rfp_name = models.CharField(max_length=255)
#     description = models.TextField()
#     service_categories = models.ManyToManyField(ServiceCategory)
#     job_type = models.CharField(choices=RFP_JOB_TYPE_CHOICES, max_length=255)
#     submission_deadline = models.DateTimeField()
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#     contact_person = models.CharField(max_length=255)
#     contact_department = models.CharField(max_length=255)
#     rfp_status = models.CharField(choices=RFP_STATUS_CHOICES, max_length=255)
#     work_scope_doc = models.FileField(upload_to='work_scope_docs/')
#     service_region = models.CharField(max_length=255)
#     require_written_proposal = models.BooleanField(default=False)


class SOWItem(models.Model):
    rfp = models.ForeignKey(RFP, on_delete=models.CASCADE)
    sow_item_id = models.AutoField(primary_key=True)
    sow_item_name = models.CharField(max_length=255)
    sow_item_desc = models.TextField()
    sow_item_budget = models.DecimalField(decimal_places=2, max_digits=10)
    sow_item_doc = models.FileField(upload_to='sow_item_docs/')


class VendorQualification(models.Model):
    VQ_TYPE_CHOICES = [
        ('preferred', 'Preferred'),
        ('required', 'Required'),
    ]
    vq_id = models.AutoField(primary_key=True)
    rfp = models.ForeignKey(RFP, on_delete=models.CASCADE)
    vq_name = models.CharField(max_length=255)
    vq_desc = models.TextField()
    vq_type = models.CharField(choices=VQ_TYPE_CHOICES, max_length=255)


class VendorResponse(models.Model):
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    rfp = models.ForeignKey(RFP, on_delete=models.CASCADE)
    response_date = models.DateTimeField()
    response_doc = models.FileField(upload_to='vendor_response_docs/')


class EvaluationCriteria(models.Model):
    rfp = models.ForeignKey(RFP, on_delete=models.CASCADE)
    criteria_id = models.AutoField(primary_key=True)
    criteria_name = models.CharField(max_length=255)
    criteria_weight = models.FloatField()


class EvaluationScore(models.Model):
    rfp = models.ForeignKey(RFP, on_delete=models.CASCADE)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    criteria = models.ForeignKey(EvaluationCriteria, on_delete=models.CASCADE)
    score_id = models.AutoField(primary_key=True)
    score_value = models.FloatField()


class AwardedRFP(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    rfp = models.ForeignKey(RFP, on_delete=models.CASCADE)
    date_awarded = models.DateField()
    proposal = models.FileField(upload_to='rfp/proposals/')
    notes = RichTextField(blank=True, null=True)

    def __str__(self):
        return f"Awarded RFP {self.rfp.rfp_name} to {self.vendor.name}"