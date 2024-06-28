from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
from rest_authtoken import auth
from rest_framework.decorators import api_view
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserCreationSerializer, LoginSerializer
from .models import CustomUser

# Create your views here.

class Authentication(generics.GenericAPIView):
    def get(self, request):
        return Response(data={"message": "Hello authentication"}, status=status.HTTP_200_OK)


# CREATING MANUALLY TOKEN
class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [
        permissions.AllowAny]
    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')
                user = authenticate(username=email, password=password)
                if user is None:
                    return Response({"data":{},"message": "user is not found"}, status=status.HTTP_400_BAD_REQUEST)

                refresh = RefreshToken.for_user(user)
                return Response({'message': "user logged in successfully","data": {"email": email},
                                'refresh': str(refresh), 'access': str(refresh.access_token)})
            return Response({'data':serializer.errors,"message":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)





class SignUp(generics.GenericAPIView):
    serializer_class = UserCreationSerializer
    permission_classes = [
        permissions.AllowAny]
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



