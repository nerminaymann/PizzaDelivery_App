from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer


# Create your views here.

class OrderList(generics.GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(data= serializer.errors,status=status.HTTP_400_BAD_REQUEST)

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





