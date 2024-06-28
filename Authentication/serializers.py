from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import CustomUser
from phonenumber_field.serializerfields import PhoneNumberField

class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=80)
    phone_number = PhoneNumberField(allow_blank=False,allow_null=False)
    password = serializers.CharField(min_length=8,write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', "password", 'password', 'phone_number']

    def validate(self, data):
        username = CustomUser.objects.filter(username=data['username'])
        if username.exists():
            raise serializers.ValidationError("username already taken")

        email = CustomUser.objects.filter(email=data['email'])
        if email.exists():
            raise serializers.ValidationError("email already taken")

        # password = data['password']
        # if password != data['password']:
        #     raise serializers.ValidationError("passwords don't match")

        password = CustomUser.objects.filter(password=data['password'])

        # if password and password[0].lower() != password[1].lower():
        #     raise serializers.ValidationError("passwords don't match")

        phone_number = CustomUser.objects.filter(phone_number=data['phone_number'])
        if phone_number.exists():
            raise serializers.ValidationError("phone number already taken")

        return super().validate(data)


    # TO MAKE SURE THAT THE NEW USER IS ACTIVE & PASSWORD IS HASHED
    #create an USER OBJ
    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    # def validate_password(self,value:str) -> str:
    #     return make_password(value)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField()


#CUSTOMIZING TOKEN SERIALIZER
class CustomTokenSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    def validate(self, email, password):
        try:
            self.user = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist as e:
            message = {'error': f'User with email={email} does not exist.'}
            return message
        check_auth = authenticate(email=email, password=password)
        if check_auth is None:
            message = {'error':
                       'The user exists, but the password is incorrect.'}
            return message
        data = self.user.jwt_tokens
        update_last_login(None, self.user)
        return data





