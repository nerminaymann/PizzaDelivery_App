from django.contrib import admin
from .models import Order,PizzaFlavour,PizzaSizePrices

# Register your models here.

admin.site.register(Order)
admin.site.register(PizzaFlavour)
admin.site.register(PizzaSizePrices)