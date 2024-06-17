from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.response import Response


# Create your views here.

class AuthenticationList(generics.GenericAPIView):
    def get(self, request):
        return Response(data={"message": "Hello authentication"}, status=status.HTTP_200_OK)
