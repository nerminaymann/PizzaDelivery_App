from django.contrib import admin
from .models import Order,PizzaFlavour,PizzaSizePrices

# Register your models here.

admin.site.register(PizzaFlavour)
admin.site.register(PizzaSizePrices)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','flavour','size','order_status','shipping_address','created_at']
    list_filter = ['order_status','size','created_at']
