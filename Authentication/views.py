from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserCreationSerializer
from .models import CustomUser

# Create your views here.

class Authentication(generics.GenericAPIView):
    def get(self, request):
        return Response(data={"message": "Hello authentication"}, status=status.HTTP_200_OK)

class SignUp(generics.GenericAPIView):
    serializer_class = UserCreationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
