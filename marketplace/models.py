from django.db import models
from accounts.models import User
from menu.models import Vw_product

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Vw_product, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.user