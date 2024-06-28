from django.conf.global_settings import AUTHENTICATION_BACKENDS
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from .models import Order
from .serializers import OrderSerializer,UpdateStatusSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


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
    Permission_classes = [IsAdminUser]
    def get_order(self,request,pk):
        order = get_object_or_404(Order, id=pk)
        serializer = OrderSerializer(order,many=False)
        return Response(data = serializer.data,status=status.HTTP_200_OK)

    def put_order(self,request,pk):
        order = get_object_or_404(Order, id=pk)
        user = request.user
        serializer = OrderSerializer(data=request.data,instance=Order)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(self.get_order(order,pk),status=status.HTTP_200_OK)
        return (serializer.errors)

    def delete_order(self,request,pk):
        order = Order.objects.get(id=pk)
        order.delete()
        return Response({"message":"the order is deleted successfully "},status=status.HTTP_204_NO_CONTENT)

#after user clicked on CheckOut Button
class UpdateStatus_CheckOutButton(generics.UpdateAPIView):
    serializer_class = UpdateStatusSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]

    def get_order(self,request,pk):
        order = Order.objects.get(id=pk)
        serializer = OrderSerializer(order,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def patch_order_status(self,request,pk):
        order = get_object_or_404(Order,id=pk)
        user = request.user
        order.order_status = "In Transit"
        order.save()
        serializer = self.get_serializer(order,instance=Order)
        if serializer.is_valid():
            serializer.save(user)
            self.perform_update(serializer)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return (serializer.errors,status.HTTP_400_BAD_REQUEST)

        # this will return order's data as a response
        return Response(self.get_order(order,pk),status=status.HTTP_200_OK)


class UserOrdersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_user_orders(self,request,user_id):
        request.user.id = user_id
        orders = Order.objects.filter(user=user_id)
        serializer = self.serializer_class(orders, many=True)
        if serializer is not None:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("you've not made orders yet, try again",status=status.HTTP_400_BAD_REQUEST)


class UserOrderDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_user_specific_orders(self,request,user_id,pk):
        request.user.id = user_id
        order = Order.objects.filter(user=user_id,pk=pk).first()
        serializer = self.serializer_class(order, many=False)
        if serializer is not None:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("order doesn't exist, please try again",status=status.HTTP_400_BAD_REQUEST)
