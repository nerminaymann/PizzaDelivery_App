from rest_framework import serializers

from Orders.models import Order,PizzaFlavour
from Authentication.models import CustomUser



class OrderSerializer(serializers.ModelSerializer):
    size = serializers.CharField(max_length=50)
    order_status = serializers.HiddenField(default='Pending')
    # flavour = serializers.CharField(source='flavour.flavour')
    quantity = serializers.IntegerField(default=0)
    # user = serializers.CharField(source='user.email', read_only=True)
    shipping_address = serializers.CharField(max_length=100)

    class Meta:
        model = Order
        fields = ["flavour","size", "quantity","order_status",'shipping_address']

class UpdateStatusSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['order','user', 'order_status']
