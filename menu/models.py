from django.db import models
from vendor.models import Vendor
from accounts.models import User, UserProfile

# Create your models here.

class Category(models.Model):
    vendor          = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name   = models.CharField(max_length=50, unique=True)
    slug            = models.SlugField(max_length=100, unique=True)
    description     = models.TextField(max_length=250, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta():
        verbose_name        = 'category'
        verbose_name_plural = 'categories'
        
        
    def clean(self):
        self.category_name = self.category_name.capitalize()
         

    def __str__(self):
        return self.category_name


class Product(models.Model):
    vendor          = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_name    = models.CharField(max_length=50)
    slug            = models.SlugField(max_length=100, unique=True)
    description     = models.TextField(max_length=250, blank=True)
    price           = models.DecimalField(max_digits=10, decimal_places=2)
    prod_photo      = models.ImageField(upload_to='prodimages')
    is_available    = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    
# class Vw_category(models.Model):
#     BUYER = 'Buyer'
#     VENDOR = 'Vendor'
#     CATEGORY_CHOICES = (
#         (BUYER, 'Buyer'),
#         (VENDOR, 'Vendor'),
#     )
#     category_name   = models.CharField(max_length=50, unique=True)
#     category_type   = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
#     slug            = models.SlugField(max_length=100, unique=True)
#     description     = models.TextField(max_length=250, blank=True)
#     created_at      = models.DateTimeField(auto_now_add=True)
#     updated_at      = models.DateTimeField(auto_now=True)

#     class Meta():
#         verbose_name        = 'vw_category'
#         verbose_name_plural = 'vw_categories'
        
        
#     def clean(self):
#         self.category_name = self.category_name.capitalize()     

#     def __str__(self):
#         return self.category_name


class Vw_product(models.Model):
    BUYER = 'Buyer'
    VENDOR = 'Vendor'
    CATEGORY_CHOICES = (
        (BUYER, 'Buyer'),
        (VENDOR, 'Vendor'),
    )
    category            = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    product_name        = models.CharField(max_length=50)
    slug                = models.SlugField(max_length=100, unique=True)
    description         = models.TextField(max_length=250, blank=True)
    price               = models.DecimalField(max_digits=10, decimal_places=2)
    price_description   = models.CharField(max_length=50, blank=True)
    is_available        = models.BooleanField(default=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    is_subscription     = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product_name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Vw_product, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Vw_product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    invoice = models.OneToOneField('Invoice', on_delete=models.SET_NULL, null=True, blank=True, related_name='order_invoice')


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='invoices')
    product = models.ForeignKey(Vw_product, on_delete=models.CASCADE, related_name='invoice_product')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
