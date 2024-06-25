from django.conf.global_settings import AUTHENTICATION_BACKENDS
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer,UpdateStatusSerializer


# Create your views here.

class OrderList(generics.GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.all()
        serializer = self.serializer_class(orders, many=True)
        # serializer = OrderSerializer(orders, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        # user = request.data.get("user")
        user = request.user
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, pk=None):
    #     order = Order.objects.get(id=pk)
    #     serializer = OrderSerializer(data=request.data,instance=order)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(self.get_serializer(instance=order).data,status=status.HTTP_200_OK)
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    def get_order(self,request,pk):
        order = Order.objects.get(id=pk)
        serializer = OrderSerializer(order,many=False)
        return Response(data = serializer.data,status=status.HTTP_200_OK)

    def put_order(self,request,pk):
        order = Order.objects.get(id=pk)
        serializer = OrderSerializer(data=request.data,instance=Order)
        if serializer.is_valid():
            serializer.save()
            return Response(self.get_order(order,pk),status=status.HTTP_200_OK)
        return (serializer.errors)

    def delete_order(self,request,pk):
        order = Order.objects.get(id=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#after user clicked on CheckOut Button
class UpdateStatus_CheckOutButton(generics.UpdateAPIView):
    serializer_class = UpdateStatusSerializer
    queryset = Order.objects.all()

    def get_order(self,request,pk):
        order = Order.objects.get(id=pk)
        serializer = OrderSerializer(order,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    # def patch_order_status(self,request,pk):
    #     order = get_object_or_404(Order,id=pk)
    #     data = {"order_status": 'In Transit'}
    #     serializer = UpdateStatusSerializer(data=data,instance=Order)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(self.get_order(order,pk),status=status.HTTP_200_OK)
    #     return (serializer.errors,status.HTTP_400_BAD_REQUEST)

    def patch_order_status(self,pk, request, *args, **kwargs):
        order = get_object_or_404(Order, id=pk)
        order_status = kwargs.pop('order_status', "In Transit")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, order_status=order_status)
        if serializer.is_valid():
            serializer.save()
            return Response(self.get_order(order,pk),status=status.HTTP_200_OK)
        return (serializer.errors, status.HTTP_400_BAD_REQUEST)
