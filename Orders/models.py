from django.db import models
# from mptt.fields import TreeForeignKey
# from mptt.models import MPTTModel , TreeForeignKey
from Authentication.models import CustomUser

# Create your models here.

order_status=[("Pending","Pending"),("In Transit","In Transit"),("Delivered","Delivered"),("Cancelled","Cancelled")]
pizza_size = [("Small","Small"),("Medium","Medium"),("Large","Large"),("Extra Large","Extra Large")]

# class PizzaFlavour(MPTTModel):
#     flavour = models.CharField(max_length=50)
#     parent = TreeForeignKey('self', null=True, blank=True,on_delete=models.PROTECT)
#
#     class MPTTMeta:
#         order_insertion_by = ['flavour']
#
#     def __str__(self):
#         return self.flavour

class PizzaFlavour(models.Model):
    flavour = models.CharField(max_length=50)
    def __str__(self):
        return self.flavour


class PizzaSizePrices(models.Model):
    flavour = models.ForeignKey('PizzaFlavour', on_delete=models.CASCADE)
    small_price = models.DecimalField(max_digits=5, decimal_places=2)
    medium_price = models.DecimalField(max_digits=5, decimal_places=2)
    large_price = models.DecimalField(max_digits=5, decimal_places=2)
    extra_large_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.flavour.flavour

class Order(models.Model):
    size = models.CharField(max_length=50, choices=pizza_size,default='')
    order_status = models.CharField(max_length=50, choices=order_status,default='')
    flavour = models.ForeignKey(PizzaFlavour,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    shipping_address=models.CharField(max_length=100)

    def __str__(self):
        return self.user.email

